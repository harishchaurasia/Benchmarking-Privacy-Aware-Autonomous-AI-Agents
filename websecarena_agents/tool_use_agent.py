from agentlab.agents.tool_use_agent.tool_use_agent import GeneralHints, Goal, Obs, PromptConfig, Summarizer, TaskHint, ToolUseAgentArgs

from config.websecarena_models import WEBSECARENA_LLAMA


DEFAULT_PROMPT_CONFIG = PromptConfig(
    tag_screenshot=False,
    goal=Goal(goal_as_system_msg=True),
    obs=Obs(
        use_last_error=True,
        use_screenshot=False,
        use_axtree=True,
        use_dom=False,
        use_som=False,
        use_tabs=False,
    ),
    summarizer=Summarizer(do_summary=True),
    general_hints=GeneralHints(use_hints=False),
    task_hint=TaskHint(use_task_hint=False),
    keep_last_n_obs=None,
    multiaction=False,  # whether to use multi-action or not
    action_subsets=("bid",),
    # action_subsets=("coord",),
    # action_subsets=("coord", "bid"),
)

TOOL_USE_LLAMA_AGENT = ToolUseAgentArgs(
    model_args=WEBSECARENA_LLAMA,
    config=DEFAULT_PROMPT_CONFIG,
)