from agentlab.experiments.study import make_study

from websecarena_benchmark import WEBSECARENA_BENCHMARK
from websecarena_generic_agents import WEBSECARENA_LLAMA_AGENT, WEBSECARENA_QWEN_AGENT, WEBSECARENA_OPENAI_AGENT, WEBSECARENA_MISTRALAI_AGENT, WEBSECARENA_DEEPSEEK_AGENT

baseline_study = make_study(
    benchmark=WEBSECARENA_BENCHMARK,  # your registered task
    agent_args=[
        WEBSECARENA_LLAMA_AGENT,
        # WEBSECARENA_QWEN_AGENT, 
        # WEBSECARENA_OPENAI_AGENT, 
        # WEBSECARENA_MISTRALAI_AGENT, 
        # WEBSECARENA_DEEPSEEK_AGENT
    ]
)

baseline_study.run(n_jobs=1, exp_root="./studies/baseline_agents")