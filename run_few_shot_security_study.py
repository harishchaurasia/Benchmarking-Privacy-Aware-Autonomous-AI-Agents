
from agentlab.experiments.study import make_study

from calc_metrics import compute_rates, latest_subdir
from websecarena_benchmark import WEBSECARENA_BENCHMARK
from websecarena_agents.few_shot_security_agents import FEW_SHOT_SECURITY_AGENT_QWEN, FEW_SHOT_SECURITY_AGENT_OPENAI, FEW_SHOT_SECURITY_AGENT_MISTRALAI, FEW_SHOT_SECURITY_AGENT_DEEPSEEK, FEW_SHOT_SECURITY_AGENT_LLAMA

study_folder = "will-studies/few_shot_security_agents/prompt-injection"

agent = [
    # FEW_SHOT_SECURITY_AGENT_LLAMA,
    # FEW_SHOT_SECURITY_AGENT_QWEN,
    FEW_SHOT_SECURITY_AGENT_OPENAI,
    # FEW_SHOT_SECURITY_AGENT_MISTRALAI,
    # FEW_SHOT_SECURITY_AGENT_DEEPSEEK,
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
