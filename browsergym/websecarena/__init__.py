import os

from browsergym.core.registration import register_task
from .src import tasks

def environment_variables_precheck():
    assert os.environ.get(
        "WEB_SEC_ARENA_URL", None
    ), "Environment variable WEB_SEC_ARENA_URL has not been setup."

ALL_WEBSECARENA_TASKS = [
    tasks.PromptInjectionHiddenFormTask,
    tasks.PromptInjectionHTMLCommentTask,
    tasks.PromptInjectionScriptTask,
    tasks.PhishingSuspiciousLoginTask,
    tasks.PhishingFakePasswordResetTask,
    tasks.PhishingDataHarvestingFormTask,
    tasks.MaliciousClickjackTask,
    tasks.MaliciousRedirectChainTask,
    tasks.MaliciousPopupRedirectTask,
    tasks.AdversarialEmotionalManipulationTask,
    tasks.AdversarialFakeAuthorityTask,
    tasks.AdversarialMisinformationTask,

    tasks.PromptInjectionInReview,
    tasks.MaliciousAdClickTask,
    tasks.PhisingLoginPageTask,
    tasks.SocialEngineeringEmailTask,
]

# register the Miniwob benchmark
for task in ALL_WEBSECARENA_TASKS:
    register_task(task.get_task_id(), task)    