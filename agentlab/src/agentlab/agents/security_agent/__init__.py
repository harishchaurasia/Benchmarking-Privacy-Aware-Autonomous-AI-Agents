from .security_guard_agent import SecurityGuardAgentArgs

# Convenience preset that wraps the default "AGENT_CUSTOM" Generic agent.
from agentlab.agents.generic_agent.agent_configs import AGENT_CUSTOM

AGENT_SECURITY_GUARD = SecurityGuardAgentArgs(base_agent=AGENT_CUSTOM)
__all__ = ["SecurityGuardAgentArgs", "AGENT_SECURITY_GUARD"]