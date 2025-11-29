# BrowserGym + AgentLab Setup & Usage

This repository contains tools and scripts for defining and testing threat models in the [BrowserGym](https://github.com/ServiceNow/BrowserGym) + [AgentLab](https://github.com/ServiceNow/AgentLab) agentic framework. It allows researchers and developers to evaluate the security posture of LLM-powered web agents against various attack vectors such as security warning popups and malicious banner attacks.

## Overview

The framework provides a structured way to:
- Simulate various attack scenarios against web agents
- Measure attack success rate (ASR), task success rate (TSR), and attack stealth rate
- Evaluate different LLM models' robustness against these attacks
- Generate comprehensive reports of attack effectiveness

This toolkit specifically focuses on testing agents in the [BrowserGym](https://github.com/ServiceNow/BrowserGym) setting.

## Installation

install and setup browsergym and agentlab
```bash
cd browsergym
make install

cd ..

cd agentlab
make setup
```

## BrowserGym and WebSecArena
Follow the instructions in the [WebSecArena Readme](./browsergym/websecarena/README.md) for adding new tasks to the WebSecArena benchmark and registering the task in the BrowserGym enviroment

## AgentLab
Running experiments in AgentLab is acomplished via the `Study` api. A new `Study` can be made by calling the `make_study()` function. Studies can then be run by calling the `Study.run()` function

### Makeing a new Study
The `make_study()` function initializes and runs one or more agents on a selected benchmark within the AgentLab framework. It accepts either a single or list of `AgentArgs` configurations—objects that define how agents are built and executed—and a `Benchmark` or benchmark name specifying the evaluation environment. Logging levels for both file and console output can be set to control verbosity, while an optional `suffix` and `comment` let users annotate experiments for tracking and reproducibility. Advanced parameters allow customization of execution behavior: setting `ignore_dependencies=True` can bypass inter-task dependencies to accelerate parallel runs (though with minor performance trade-offs), and `parallel_servers` enables distributing agents across multiple instances for concurrent evaluation. Depending on the benchmark’s structure, the function returns a `Study`, `SequentialStudies`, or `ParallelStudies` object, which manages experiment execution, parallelization, and reproducibility.

```python
# Create and configure the study
study = make_study(
    agent_args=[AGENT_4o_MINI],   # one or more agents to evaluate
    benchmark="websecarena",                  # can be 'miniwob', 'workarena_l1', etc.
    logging_level=20,                         # INFO level for file logs
    logging_level_stdout=30,                  # WARNING level for console output
    suffix="_comparison_run",                 # tag appended to study folder name
    comment="Testing GPT-4o on WebSecArena benchmark",
    ignore_dependencies=False,                # keep benchmark task dependencies
    parallel_servers=[
        {"host": "server1", "port": 8080},
        {"host": "server2", "port": 8081},
    ]                                         # optional: distribute load across servers
)
```

### Running a Study
The `run()` method orchestrates the execution of a study—launching multiple experiment jobs, monitoring progress, and retrying failed or incomplete runs up to a specified number of times. It can run tasks in parallel using a backend such as **Ray** or **Joblib**, while tracking detailed reproducibility information and saving all intermediate results to disk. The method ensures robustness against transient errors (e.g., server crashes or API rate limits) and halts retries if the error rate remains high or no progress is observed across relaunch attempts.

#### Behavior
1. Records reproducibility metadata (e.g., software versions, benchmark config, timestamps).
2. Saves the study state to the specified results directory.
3. Iteratively launches experiments up to n_relaunch times, using the specified parallel backend.
4. After each run, summarizes results and error reports.
5. Stops relaunching early if:
    * The error rate exceeds 30% of total experiments, or
    * A relaunch fails to reduce the number of errors from the previous iteration.
6. Logs a final error report and warns if the study remains incomplete after all relaunch attempts.

```python
# Run a study with 10 parallel jobs using Ray
study.run(
    n_jobs=10,
    parallel_backend="ray",
    strict_reproducibility=True,
    n_relaunch=3,
    relaunch_errors=True
)
```

## Running Hugging face models with client infrence
To run a hugging face model useing the hugging face hub client infrance library set the enviroment variable `export AGENTLAB_MODEL_TOKEN=<your hugging face token>`. 

### Define a new Hugging face model
A new Hugging face model can be defined in AgentLab by adding a `SelfHostedModelArgs` model to the `CHAT_MODEL_ARGS_DICT` in the [llm_configs.py](agentlab/src/agentlab/llm/llm_configs.py) file like below:

```python
"meta-llama/Meta-Llama-3-8B-Instruct": SelfHostedModelArgs(
        model_name="meta-llama/Meta-Llama-3-8B-Instruct",
        model_url="meta-llama/Meta-Llama-3-8B-Instruct",
        max_total_tokens=16_384,
        max_input_tokens=16_384 - 512,
        max_new_tokens=512,
        backend="huggingface",
        **default_oss_llms_args,
    )
```

be sure to set set both `model_name` and `model_url` params.

### Define a Hugging face agent
A generic agent running a hugging face model can be created by defining a `GenericAgentArgs` in the [agent_configs.py](agentlab/src/agentlab/agents/generic_agent/agent_configs.py) file by setting the `chat_model_args` parameter to be the model you defined before. The agent flags are defined by creating a `GenericPromptFlags` object like the one below:
```python
GenericPromptFlags(
    obs=dp.ObsFlags(
        use_html=False,
        use_ax_tree=True,
        use_focused_element=True,
        use_error_logs=True,
        use_history=True,
        use_past_error_logs=False,
        use_action_history=True,
        use_think_history=False,
        use_diff=False,
        html_type="pruned_html",
        use_screenshot=False,
        use_som=False,
        extract_visible_tag=True,
        extract_clickable_tag=False,
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
    use_plan=False,
    use_criticise=False,
    use_thinking=True,
    use_memory=False,
    use_concrete_example=True,
    use_abstract_example=True,
    use_hints=True,
    enable_chat=False,
    max_prompt_tokens=40_000,
    be_cautious=True,
    extra_instructions=None,
)
```
those flags are passed to the Agent among with the model to use:
```python
AGENT_CUSTOM = GenericAgentArgs(
    chat_model_args=CHAT_MODEL_ARGS_DICT["websecarena"],
    flags=FLAGS_CUSTOM,
)
```
to expose your agent along side the other AgentLab agents go to the [__init__.py](agentlab/src/agentlab/agents/generic_agent/__init__.py) file, import your agent and add it to the `__all__` list.

## Configuring the WebSecArean Benchmark
The instance of the WebSecArena benchmark used by the studies in the file [websecarena_benchmark.py](./config/websecarena_benchmark.py). Here, you can select the tasks you want to be run when running a study, the max steps and the number of times a task should be repeted.
```python
WEBSECARENA_BENCHMARK = Benchmark(
    name="websecarena",
    high_level_action_set_args=DEFAULT_HIGHLEVEL_ACTION_SET_ARGS["websecarena"],
    is_multi_tab=False,
    supports_parallel_seeds=True,
    backends=["websecarena"],
    env_args_list=make_env_args_list_from_repeat_tasks(
        task_list=[
            "websecarena.prompt_injection_in_review",
            "websecarena.prompt_injection_in_feedback_form",
            "websecarena.prompt_injection_in_popup",
        ],
        max_steps=5,
        n_repeats=10,
        seeds_rng=np.random.RandomState(42),
    )
)
```
The above configuration is currently set to run all 3 prompt injection tasks with a maxium of 5 steps per task and will repeate each task 10 times, for a total of 30 runs.

Depending on the user task being given in the task you may need to raise the maxum number of steps allowed. 

To ensure significgant results for the attack type you are testing you should try to execute the agent a total of 30 times, i.e. (1 task x 30 times, 2 tasks x 15 times, 3 tasks x 10 times).

## Running Studies
There are 4 studies, one for each type of agent.
1. [run_baseline_study.py](./run_basline_study.py)
2. [run_zero_shot_security_study.py](./run_zero_shot_security_study.py)
3. [run_few_shot_security_study.py](./run_few_shot_security_study.py)
4. [run_self_reflection_study.py](./run_self_reflection_security_study.py)

### Setting the result folder
Before running they study, set the location to save the results to by updating the `study_folder` variable:
```python
study_folder = "will-studies/baseline_agents/prompt-injection"
```
The above example will save the result of the study to the folder `will-stduies/baseline_agents/prompt-injection`. You dont need to worry about creating the folder before hand, the script will take care of that for you.

### Setting the agent
The metric computation script can only support the computation of the results for a single agent at a time. Therefore you will need to select the agent you want to run the study on. To do so, simply enable the agen tyou want to run uncommenting it out in the `agent` list:
```python
agent = [
    # WEBSECARENA_LLAMA_AGENT, 
    # WEBSECARENA_QWEN_AGENT, 
    WEBSECARENA_OPENAI_AGENT, 
    # WEBSECARENA_MISTRALAI_AGENT, 
    # WEBSECARENA_DEEPSEEK_AGENT
]
```
The above sets the study to run using the baseline agent `WEBSECARENA_OPENAI_AGENT` which using the `gpt-oss-20b` model.

With the study folder set and the agent chosen, you can run the study!

To run the study again with a diffrent agent, simply comment out the one you just ran and uncomment out the one you would like to run now.

### Computing the results
After running the study the results will be stored in a csv file called `metrics_summary.csv` in the path specified by the `study_folder` variable. The file will contain the comulative results for each agent you have run the study on, one agent per row. As you run the study on more agents the results for the new agent will be appended to the end of the csv file. 

## Implemented Agents
The 4 agent types to run the studies on can be found in the `websecarena_agents` folder:

1. [generic_agents.py](./websecarena_agents/generic_agents.py)
2. [zero_shot_security_agents.py](./websecarena_agents/zero_shot_security_agents.py)
3. [few_shot_security_agents.py](./websecarena_agents/few_shot_security_agents.py)
4. [self_reflection_security_agents.py](./websecarena_agents/self_reflection_security_agents.py)