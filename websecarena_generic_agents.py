from agentlab.agents.generic_agent.generic_agent import GenericAgentArgs
from agentlab.agents.generic_agent.generic_agent_prompt import GenericPromptFlags
from agentlab.agents import dynamic_prompting as dp
from browsergym.experiments.benchmark.base import HighLevelActionSetArgs

from websecarena_models import WEBSECARENA_LLAMA, WEBSECARENA_DEEPSEEK, WEBSECARENA_MISTRALAI, WEBSECARENA_OPENAI, WEBSECARENA_QWEN


websecarena_flags = GenericPromptFlags(
    obs=dp.ObsFlags(
        use_html=False,  # too big for most benchmark except miniwob
        use_ax_tree=True,  # very useful
        use_focused_element=False,  # detrimental on minowob according to ablation study
        use_error_logs=True,
        use_history=True,
        use_past_error_logs=False,  # very detrimental on L1 and miniwob
        use_action_history=True,  # helpful on miniwob
        use_think_history=False,  # detrimental on L1 and miniwob
        use_diff=False,
        html_type="pruned_html",
        use_screenshot=False,
        use_som=False,
        extract_visible_tag=True,  # doesn't change much
        extract_clickable_tag=False,  # doesn't change much
        extract_coords="False",
        filter_visible_elements_only=False,
    ),
    action=dp.ActionFlags(
        action_set=HighLevelActionSetArgs(
            subsets=["bid"],
            multiaction=False,
        ),
        long_description=False,
        individual_examples=True,
    ),
    use_plan=False,  # usually detrimental
    use_criticise=False,  # usually detrimental
    use_thinking=True,  # very useful
    use_memory=False,
    use_concrete_example=True,  # useful
    use_abstract_example=True,  # useful
    use_hints=True,  # useful
    enable_chat=False,
    max_prompt_tokens=40_000,
    be_cautious=True,
    extra_instructions=None,
)

WEBSECARENA_LLAMA_AGENT = GenericAgentArgs(
    chat_model_args=WEBSECARENA_LLAMA,
    flags=websecarena_flags,
)

WEBSECARENA_QWEN_AGENT = GenericAgentArgs(
    chat_model_args=WEBSECARENA_QWEN,
    flags=websecarena_flags,
)

WEBSECARENA_OPENAI_AGENT = GenericAgentArgs(
    chat_model_args=WEBSECARENA_OPENAI,
    flags=websecarena_flags,
)

WEBSECARENA_MISTRALAI_AGENT = GenericAgentArgs(
    chat_model_args=WEBSECARENA_MISTRALAI,
    flags=websecarena_flags,
)

WEBSECARENA_DEEPSEEK_AGENT = GenericAgentArgs(
    chat_model_args=WEBSECARENA_DEEPSEEK,
    flags=websecarena_flags,
)