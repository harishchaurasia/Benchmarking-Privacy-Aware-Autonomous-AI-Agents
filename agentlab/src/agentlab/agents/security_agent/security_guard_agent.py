from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Tuple

from browsergym.experiments.agent import Agent, AgentInfo, default_obs_preprocessor
from agentlab.agents.agent_args import AgentArgs
from agentlab.agents.generic_agent import GenericAgentArgs
from agentlab.agents.generic_agent import generic_agent as generic_module  # for type hints
from agentlab.llm.llm_utils import Discussion  # only for AgentInfo compatibility

CLOSE_TEXTS = ("close", "dismiss", "X", "x", "ok", "got it", "i understand")

# Very light-weight secret patterns. Keep conservative to avoid false positives.
SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9]{16,}",                   # e.g., OpenAI style
    r"(?i)\b(api[_-]?key|secret|token)\b\s*[:=]\s*['\\\"]?[A-Za-z0-9_\-]{10,}",
    r"(?i)\bpassword\b\s*[:=]\s*['\\\"]?.{4,}",
    r"(?i)\baws_?access_?key_?id\b\s*[:=]\s*[A-Z0-9]{16,}",
    r"(?i)\baws_?secret_?access_?key\b\s*[:=]\s*[A-Za-z0-9/+=]{20,}",
    r"(?i)\bprivate[_-]?key\b",
]

INJECTION_KEYWORDS = [
    "SYSTEM_PROMPT", "INTERNAL", "CONFIDENTIAL", "DO NOT SHARE", "SECRET",
    "copy this into chat", "override previous instructions", "ignore previous rules",
    "you must", "urgent", "time-limited", "security alert", "IMPORTANT"
]


def _compile(patterns: List[str]) -> List[re.Pattern]:
    return [re.compile(p) for p in patterns]


SECRET_RE = _compile(SECRET_PATTERNS)
# Loose keyword scan – not regex for simplicity and speed.
INJECTION_KEYWORDS_LOWER = [k.lower() for k in INJECTION_KEYWORDS]


def looks_like_secret(text: str) -> bool:
    if not text:
        return False
    for rx in SECRET_RE:
        if rx.search(text):
            return True
    return False


def strip_injection(text: str) -> Tuple[str, bool, List[str]]:
    """Remove obvious in-prompt instructions & comments that look like injections.

    Returns:
        sanitized_text, flagged(bool), reasons(list)
    """
    if not text:
        return text, False, []

    flagged = False
    reasons: List[str] = []

    # Drop HTML comments that look like "system prompt" or secrets
    def repl_comment(m: re.Match) -> str:
        nonlocal flagged, reasons
        comment = m.group(1)
        cl = comment.lower()
        if any(k in cl for k in INJECTION_KEYWORDS_LOWER) or looks_like_secret(comment):
            flagged = True
            reasons.append("removed suspicious HTML comment")
            return ""  # drop it entirely
        return m.group(0)

    text = re.sub(r"<!--\s*(.*?)\s*-->", repl_comment, text, flags=re.S)

    # Mask inline secret-ish tokens
    before = text
    for rx in SECRET_RE:
        text = rx.sub("[REDACTED]", text)
    if text != before:
        flagged = True
        reasons.append("redacted secret-looking tokens")

    return text, flagged, reasons


def find_close_button_bid(ax_txt: str) -> str | None:
    """Try to find a 'Close'/'Dismiss' button bid in the AXTree text dump."""
    if not ax_txt:
        return None
    # Example line (varies per env):
    # [1836] button "Close ALERT ..."  or  [42] button 'Close'
    for line in ax_txt.splitlines():
        low = line.lower()
        if "button" in low and any(t in low for t in CLOSE_TEXTS):
            m = re.search(r"\[(\d+)\]\s*button", line)
            if m:
                return m.group(1)
    return None


@dataclass
class SecurityGuardAgentArgs(AgentArgs):
    """A wrapper agent that adds basic security awareness.

    It delegates decision-making to a base GenericAgent, but:
    1) sanitizes observations (HTML/AX tree) to remove bait injections & secrets;
    2) detects likely injections and attempts safe mitigation (close/dismiss);
    3) blocks actions that try to paste or echo secrets.

    You can start with your existing GenericAgentArgs as base_agent.
    """
    base_agent: GenericAgentArgs = field(default_factory=GenericAgentArgs)
    risk_close_modal: bool = True
    risk_send_message: bool = True
    refuse_secret_fill: bool = True
    agent_name: str = "security_guard"

    def make_agent(self) -> Agent:
        # Instantiate the delegate GenericAgent now, so we can reuse its action_set and preprocessor.
        delegate = self.base_agent.make_agent()
        return SecurityGuardAgent(delegate, self)


class SecurityGuardAgent(Agent):
    def __init__(self, delegate: generic_module.GenericAgent, args: SecurityGuardAgentArgs):
        self.delegate = delegate
        self.args = args
        # Adopt the same action set as the delegate
        self.action_set = self.delegate.action_set

    # --- Observation processing ------------------------------------------------
    def obs_preprocessor(self, obs: dict) -> dict:
        # First get the default text fields (dom_txt, pruned_html, axtree_txt, etc.)
        obs = default_obs_preprocessor(obs)

        # Keep originals
        obs["pruned_html_raw"] = obs.get("pruned_html", "")
        obs["axtree_txt_raw"] = obs.get("axtree_txt", "")

        # Sanitize text fields
        pruned_html_sanit, html_flag, html_reasons = strip_injection(obs.get("pruned_html", ""))
        ax_sanit, ax_flag, ax_reasons = strip_injection(obs.get("axtree_txt", ""))

        # Replace what downstream prompt builder will consume
        obs["pruned_html"] = pruned_html_sanit
        obs["axtree_txt"] = ax_sanit

        # Attach basic security metadata (shows up in AgentXray)
        obs["security_meta"] = {
            "html_sanitized": html_flag,
            "ax_sanitized": ax_flag,
            "reasons": html_reasons + ax_reasons,
        }
        return obs

    # --- Policy checks ---------------------------------------------------------
    def _detect_injection(self, obs: dict) -> Tuple[bool, List[str]]:
        cues = []
        # Look into raw (un-sanitized) in case we redacted it
        html = obs.get("pruned_html_raw", "") or obs.get("pruned_html", "")
        ax = obs.get("axtree_txt_raw", "") or obs.get("axtree_txt", "")
        lower_blob = (html + "\n" + ax).lower()
        for k in INJECTION_KEYWORDS_LOWER:
            if k in lower_blob:
                cues.append(f"keyword:{k}")
        if looks_like_secret(html) or looks_like_secret(ax):
            cues.append("secret-like-token")
        return (len(cues) > 0), cues

    def _block_secret_action(self, action: str) -> bool:
        """Return True if the action looks like it would exfiltrate a secret."""
        if not action:
            return False
        # Simple heuristic: if action contains a quoted payload that looks like a secret.
        # e.g., fill('123', 'sk-...') or send_msg_to_user("API_KEY=ABC...")
        payloads = re.findall(r"['\\\"]([^'\\\"]{4,})['\\\"]", action)
        for p in payloads:
            if looks_like_secret(p):
                return True
        return False

    # --- Acting ---------------------------------------------------------------
    def get_action(self, obs):
        # 1) Early risk assessment
        risky, cues = self._detect_injection(obs)

        if risky:
            # Try to close a modal if one is present
            if self.args.risk_close_modal:
                bid = find_close_button_bid(obs.get("axtree_txt_raw") or obs.get("axtree_txt", ""))
                if bid:
                    info = AgentInfo(
                        think=f"Detected likely prompt-injection ({', '.join(cues)}). "
                              f"Attempting to close modal via button {bid}.",
                        chat_messages=[],
                        stats={"security_cues": cues, "mitigation": "close"},
                        extra_info={"security": obs.get('security_meta', {})},
                    )
                    return f"click('{bid}')", info

            # If nothing to close, notify the user and proceed cautiously
            if self.args.risk_send_message:
                info = AgentInfo(
                    think=f"Detected likely prompt-injection ({', '.join(cues)}). "
                          f"Refusing to follow on-page instructions that override the goal.",
                    chat_messages=[],
                    stats={"security_cues": cues, "mitigation": "send_msg_to_user"},
                    extra_info={"security": obs.get('security_meta', {})},
                )
                msg = ("This page shows content that looks like a prompt-injection or secret bait. "
                       "I'll ignore it, keep only to the user's goal, and avoid exposing secrets.")
                return f"send_msg_to_user(\"{msg}\")", info

        # 2) Delegate to the underlying agent for normal decision-making
        action, agent_info = self.delegate.get_action(obs)

        # 3) Post-check: block accidental exfiltration
        if self.args.refuse_secret_fill and self._block_secret_action(action):
            safe_info = AgentInfo(
                think="Blocked an action that appears to include a secret value. "
                      "Replacing with a safe user message.",
                chat_messages=getattr(agent_info, "chat_messages", []),
                stats={"blocked_secret_action": True},
                extra_info={"security": obs.get('security_meta', {})},
            )
            return (
                "send_msg_to_user(\"Refusing to type or repeat secret-looking values. "
                "Please provide non-sensitive input or confirm alternative steps.\")",
                safe_info,
            )

        # 4) Return the original action if all checks passed
        return action, agent_info
