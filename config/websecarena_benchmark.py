from browsergym.experiments.benchmark.base import Benchmark
from browsergym.experiments.benchmark.configs import DEFAULT_HIGHLEVEL_ACTION_SET_ARGS
from browsergym.experiments.benchmark.utils import make_env_args_list_from_repeat_tasks
import numpy as np

WEBSECARENA_BENCHMARK = Benchmark(
    name="websecarena",
    high_level_action_set_args=DEFAULT_HIGHLEVEL_ACTION_SET_ARGS["websecarena"],
    is_multi_tab=False,
    supports_parallel_seeds=True,
    backends=["websecarena"],
    env_args_list=make_env_args_list_from_repeat_tasks(
        task_list=[
            # "websecarena.prompt_injection_in_review",
            # "websecarena.prompt_injection_in_feedback_form",
            # "websecarena.prompt_injection_in_popup",
            # "websecarena.malicious_ad_click",
            # "websecarena.phishing_login_page",
            # "websecarena.social_engineering_link",
            # "websecarena.social_engineering_data",
            # "websecarena.social_engineering_attachment",
            # "websecarena.malicious_drive_by_download",
            # "websecarena.malicious_clickjack"
            # "websecarena.malicious_redirect_chain",
            "websecarena.malicious_popup_redirect",
        ],
        max_steps=6,
        n_repeats=5,
        seeds_rng=np.random.RandomState(42),
    )
)