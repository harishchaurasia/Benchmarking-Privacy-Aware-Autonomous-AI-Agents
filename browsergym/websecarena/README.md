# WebSecArena benchmark for BrowserGym

This package provides `browsergym.websecarena`, which is an official port of the [WebSecArena](https://github.com/harishchaurasia/Benchmarking-Privacy-Aware-Autonomous-AI-Agents) benchmark for BrowserGym.

## Adding new tasks
To add a new WebSecArena Task you can add the task to the [tasks.py file](./src/tasks.py) by implementing the `AbstractWebSecArenaTask` class, setting the `subdomain` name and definging the `setup()` and `validate()` functions. Finially, you regesiter the task in the Broswergym inviroment in the [__init__.py file](./__init__.py).

### Subdomain
This is the name of the task you are adding it. It will be expressed as 'websecarena.[subdomain]' within the BrowserGym and AgentLab enviroments

### The `setup()` function
The `setup()` function intializes the starting state of you task. It takes in a [playwrite](https://playwright.dev) page object, which refrences the current state of the task browser enviroment. You can set the page state by using the `page.goto()` function and passing the url of the page you want to start at. You can also manually set the page content by using the `page.set_content()` function. The `setup()` function returns a 2 dimensial tuple consitsin gof the users goal, which wil be used as the inital prompt given to the agent, as well as a dict containg any context info to provide the agent with.

### The `validate()` function
The `validate()` function will be used after each agent action to check whether the agent as accomplished the users goal. It takes in the current playwrite page state and the chat messages as a list of strings. It retuns a 4 diminsonal tuple consisting of the **reward**, **done** flag, **message**, and **info**. **reward** is a floating point number used to reward the model during training. **done** is a boolean flag that is `true` if the task was completed sucessfully and `false` other wise. **message** is a string and is the new message that will be sent to the user chat. **info** is a dict that provides custom info for the task and logging purposes.

### Registering the task
You easily regester the task in the BrowserGym enviroment by simply adding it to the `ALL_WEBSECARENA_TASKS` list in the [__init__.py file](./__init__.py)

### Configuring tasks to run for the Defualt WebSecArena Benchmark
You can update the task list for the Default WebSecArena Benchmark by navigating to the [configs.py](browsergym/browsergym/experiments/src/browsergym/experiments/benchmark/configs.py) file. In the `DEFAULT_BENCHMARKS` dict, find the `websecarena` entry:

```python
"websecarena": lambda n_repeats=1: Benchmark(
        name="websecarena",
        high_level_action_set_args=DEFAULT_HIGHLEVEL_ACTION_SET_ARGS["websecarena"],
        is_multi_tab=False,
        supports_parallel_seeds=True,
        backends=["websecarena"],
        env_args_list=make_env_args_list_from_repeat_tasks(
            task_list=["websecarena.prompt_injection_hidden_form", "websecarena.prompt_injection_html_comment"],
            max_steps=5,
            n_repeats=n_repeats,
            seeds_rng=np.random.RandomState(42),
        )
    ),
```

You can edit the task to include the tasks you would like to have run by defualt for the benchmark.