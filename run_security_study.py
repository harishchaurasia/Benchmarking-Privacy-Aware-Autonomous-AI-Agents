
from agentlab.experiments.study import make_study

from websecarena_benchmark import WEBSECARENA_BENCHMARK
from websecarena_generic_agents import WEBSECARENA_LLAMA_AGENT, WEBSECARENA_QWEN_AGENT, WEBSECARENA_OPENAI_AGENT, WEBSECARENA_MISTRALAI_AGENT, WEBSECARENA_DEEPSEEK_AGENT
from websecarena_security_agents import SECURITY_AGENT_QWEN, SECURITY_AGENT_OPENAI, SECURITY_AGENT_MISTRALAI, SECURITY_AGENT_DEEPSEEK, SECURITY_AGENT_LLAMA

# -------------------------------------------------------
# 2. Configure the studies
# -------------------------------------------------------
# baseline_study = make_study(
#     benchmark=WEBSECARENA_BENCHMARK,  # your registered task
#     agent_args=[
#         WEBSECARENA_LLAMA_AGENT, 
#         # WEBSECARENA_QWEN_AGENT, 
#         # WEBSECARENA_OPENAI_AGENT, 
#         # WEBSECARENA_MISTRALAI_AGENT, 
#         # WEBSECARENA_DEEPSEEK_AGENT
#     ]
# )

security_study = make_study(
    benchmark=WEBSECARENA_BENCHMARK,  # your registered task
    agent_args=[
        SECURITY_AGENT_LLAMA,
        # SECURITY_AGENT_QWEN,
        # SECURITY_AGENT_OPENAI,
        # SECURITY_AGENT_MISTRALAI,
        # SECURITY_AGENT_DEEPSEEK,
    ]
)

# -------------------------------------------------------
# 3. Run the studies (parallel execution)
# -------------------------------------------------------
# Adjust n_jobs based on available cores
# baseline_study.run(n_jobs=1, exp_root="./studies/baseline_agents")
security_study.run(n_jobs=1, exp_root="./studies/security_agents")

# -------------------------------------------------------
# 4. Summarize results
# -------------------------------------------------------
# summary = study.get_summary()
# print("\n=== Study Summary ===")
# print(summary)

# Optionally, access detailed per-run results:
# results_df = study.get_results()
# print(results_df.head())
