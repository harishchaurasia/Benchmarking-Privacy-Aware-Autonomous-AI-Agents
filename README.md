# BrowserGym+ AgentLab Threat Models

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

### Experiment Configuration Parameters

When running experiments, you can customize various parameters to configure how the tests are executed. Here's an explanation of the key parameters that can be set:

```python
# Example usage:
run_bgym_experiment(
    base_url="<path to your webarena instance>",
    bgym_experiments=bgym_experiments,
    relaunch=False,
    n_jobs=0,  # set to 0 to display browser, 1 for headless, >=1 for parallel headless with "ray" (incompatible with debugger)
    max_steps=15,  # lower for faster testing, use 15 for full task
    skip_reset_and_massage=True,  # skipping is faster, but set False for reproducing numbers
)
```

- **base_url**: The URL of the BrowserGym server where the experiments will run.

- **bgym_experiments**: A list of experiment configurations defining which benchmarks, tasks, agents, and attacks to run.

- **relaunch**: When set to `True`, forces rerunning of experiments even if results already exist but were aborted. Default is `False` to avoid duplicate runs.

- **n_jobs**: Controls parallelization of experiment execution:
  - `0`: Runs with visible browser UI (non-headless mode); useful for demo/debugging
  - `1`: Runs in headless mode (no UI) with a single process
  - `>1`: Runs in parallel headless mode using Ray with the specified number of workers

- **max_steps**: Maximum number of steps each agent is allowed to take per task. Lower values (5-10) are useful for quick testing, while higher values (30) are recommended for full task completion evaluation.

- **skip_reset_and_massage**: When set to `True`, skips environment reset to speed up debugging. This should always be set to `False` when making experiments.

## Results

Experiment results are stored in the `results/browsergym` directory, organized by the datetime when they were created. Each results directory contains:

- Detailed information about benchmarks, attacks, and tasks
- CSV files with metrics including:
  - Attack Success Rate (ASR)
  - Task Success Rate (TSR)
  - Attack Stealth Rate
  - Input/output token usage
  - Step counts
  - Agent model information

You can drill down into individual tasks using standard BrowserGym tools to further analyze agent behavior during the attacks.
