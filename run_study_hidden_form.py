"""
AgentLab study to evaluate agents on the BrowserGym task:
browsergym/security.prompt_injection.hidden_form

Run:
    python run_study_hidden_form.py
"""

from agentlab.agents.generic_agent.generic_agent import GenericAgentArgs
from agentlab.agents.generic_agent.generic_agent_prompt import GenericPromptFlags
from agentlab.experiments.study import make_study
from agentlab.llm.chat_api import SelfHostedModelArgs
from browsergym.experiments.benchmark.base import Benchmark, HighLevelActionSetArgs
from browsergym.experiments.benchmark.configs import DEFAULT_HIGHLEVEL_ACTION_SET_ARGS
from browsergym.experiments.benchmark.utils import make_env_args_list_from_repeat_tasks
import numpy as np
from agentlab.agents import dynamic_prompting as dp

websecarena_model = SelfHostedModelArgs(
    model_name="meta-llama/Llama-3.1-8B-Instruct",
    model_url="meta-llama/Llama-3.1-8B-Instruct",
    max_total_tokens=16_384,
    max_input_tokens=16_384 - 512,
    max_new_tokens=512,
    backend="huggingface",
)

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

websecarena_agent = GenericAgentArgs(
    chat_model_args=websecarena_model,
    flags=websecarena_flags,
)

websecarena_benchmark = Benchmark(
    name="websecarena",
    high_level_action_set_args=DEFAULT_HIGHLEVEL_ACTION_SET_ARGS["websecarena"],
    is_multi_tab=False,
    supports_parallel_seeds=True,
    backends=["websecarena"],
    env_args_list=make_env_args_list_from_repeat_tasks(
        task_list=[
            # "websecarena.prompt_injection_hidden_form",
            # "websecarena.phishing_suspicious_login",
            "websecarena.malicious_clickjack"
            ],
        max_steps=5,
        n_repeats=1,
        seeds_rng=np.random.RandomState(42),
    )
)

# -------------------------------------------------------
# 2. Configure the study
# -------------------------------------------------------
study = make_study(
    benchmark=websecarena_benchmark,  # your registered task
    agent_args=[websecarena_agent],
)

# -------------------------------------------------------
# 3. Run the study (parallel execution)
# -------------------------------------------------------
# Adjust n_jobs based on available cores
study.run(n_jobs=1, exp_root="./studies/websecarena")

# -------------------------------------------------------
# 4. Summarize results
# -------------------------------------------------------
# summary = study.get_summary()
# print("\n=== Study Summary ===")
# print(summary)

# Optionally, access detailed per-run results:
# results_df = study.get_results()
# print(results_df.head())
