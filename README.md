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
