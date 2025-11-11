"""
AgentLab study to evaluate agents on the BrowserGym task:
browsergym/security.prompt_injection.hidden_form

Run:
    python run_study_hidden_form.py
"""

from agentlab.agents.generic_agent import AGENT_CUSTOM
from agentlab.experiments.study import make_study

# -------------------------------------------------------
# 2. Configure the study
# -------------------------------------------------------
study = make_study(
    benchmark="websecarena",  # your registered task
    agent_args=[AGENT_CUSTOM],
    # seeds=[0, 1, 2, 3, 4],          # 5 independent runs
    # timeout=300,                    # seconds per episode
    # max_steps=30,                   # max agent steps per episode
    # study_dir="./studies/hidden_form_study",  # output logs / metricspip
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
