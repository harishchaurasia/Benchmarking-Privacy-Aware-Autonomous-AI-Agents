# agentlab/src/agentlab/benchmarks/websecarena.py

from typing import List
from agentlab.benchmarks.abstract_env import AbstractBenchmark

# the 12 websec tasks you showed
_TASK_IDS: List[str] = [
    "browsergym/websec/sql_injection",
    "browsergym/websec/xss_reflected",
    "browsergym/websec/xss_stored",
    "browsergym/websec/csrf_basic",
    "browsergym/websec/open_redirect",
    "browsergym/websec/idor_profile",
    "browsergym/websec/idor_order",
    "browsergym/websec/auth_bypass",
    "browsergym/websec/2fa_bypass",
    "browsergym/websec/file_upload",
    "browsergym/websec/lfi_basic",
    "browsergym/websec/rate_limit",
]


class WebSecArena(AbstractBenchmark):
    """
    Minimal benchmark wrapper for BrowserGym web security tasks.

    agentlab expects: a .name and a list of "env_args" (or at least something under .env_args_list)
    but since we're just enumerating existing task IDs, we can expose a helper .task_ids()
    and leave env_args_list empty for now.
    """

    # this will also satisfy the BaseModel field
    name: str = "websecarena"
    env_args_list: list = []  # you can later fill this with real env args objects

    def get_version(self) -> int:
        # override if you want
        return 1

    # convenience method (what you were calling in the REPL)
    def task_ids(self) -> List[str]:
        return list(_TASK_IDS)
