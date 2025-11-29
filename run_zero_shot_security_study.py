
from agentlab.experiments.study import make_study

from utils.calc_metrics import compute_rates, latest_subdir
from config.websecarena_benchmark import WEBSECARENA_BENCHMARK
from websecarena_agents.zero_shot_security_agents import ZERO_SHOT_SECURITY_AGENT_QWEN, ZERO_SHOT_SECURITY_AGENT_OPENAI, ZERO_SHOT_SECURITY_AGENT_MISTRALAI, ZERO_SHOT_SECURITY_AGENT_DEEPSEEK, ZERO_SHOT_SECURITY_AGENT_LLAMA

study_folder = "will-studies/zero_shot_security_agents/prompt-injection"

agent = [
    # ZERO_SHOT_SECURITY_AGENT_LLAMA,
    # ZERO_SHOT_SECURITY_AGENT_QWEN,
    ZERO_SHOT_SECURITY_AGENT_OPENAI,
    # ZERO_SHOT_SECURITY_AGENT_MISTRALAI,
    # ZERO_SHOT_SECURITY_AGENT_DEEPSEEK,
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
