
from agentlab.experiments.study import make_study

from calc_metrics import compute_rates, latest_subdir
from websecarena_benchmark import WEBSECARENA_BENCHMARK
from websecarena_generic_agents import WEBSECARENA_LLAMA_AGENT, WEBSECARENA_QWEN_AGENT, WEBSECARENA_OPENAI_AGENT, WEBSECARENA_MISTRALAI_AGENT, WEBSECARENA_DEEPSEEK_AGENT
from websecarena_security_agents import SECURITY_AGENT_QWEN, SECURITY_AGENT_OPENAI, SECURITY_AGENT_MISTRALAI, SECURITY_AGENT_DEEPSEEK, SECURITY_AGENT_LLAMA

study_folder = "will-studies/security_agents/social-engineering"

agent = [
    SECURITY_AGENT_LLAMA,
    # SECURITY_AGENT_QWEN,
    # SECURITY_AGENT_OPENAI,
    # SECURITY_AGENT_MISTRALAI,
    # SECURITY_AGENT_DEEPSEEK,
]

security_study = make_study(
    benchmark=WEBSECARENA_BENCHMARK,  # your registered task
    agent_args=agent
)

security_study.run(n_jobs=1, exp_root=study_folder)

compute_rates(
    csv_path=f"{latest_subdir(study_folder)}/result_df_trial_1_of_3.csv",
    results_path=f"{study_folder}/metrics_summary.csv",
    model_name=agent[0].chat_model_args.model_name,
    reward_col="cum_reward",
)
