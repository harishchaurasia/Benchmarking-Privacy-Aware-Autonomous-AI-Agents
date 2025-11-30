import os

from browsergym.core.registration import register_task
from .src import tasks

def environment_variables_precheck():
    assert os.environ.get(
        "WEB_SEC_ARENA_URL", None
    ), "Environment variable WEB_SEC_ARENA_URL has not been setup."

ALL_WEBSECARENA_TASKS = [
    tasks.PhishingSuspiciousLoginTask,
    tasks.PhishingFakePasswordResetTask,
    tasks.PhishingDataHarvestingFormTask,
    tasks.MaliciousClickjackTask,
    tasks.MaliciousRedirectChainTask,
    tasks.MaliciousPopupRedirectTask,

    tasks.PromptInjectionInReview,
    tasks.PromptInjectionInFeedbackForm,
    tasks.PromptInjectionInPopup,

    tasks.MaliciousAdClickTask,
    tasks.PhisingLoginPageTask,
    
    tasks.SocialEngineeringLinkTask,
    tasks.SocialEngineeringDataTask,
    tasks.SocialEngineeringAttachmentTask,

    tasks.MaliciousDriveByDownloadTask,
]

# register the Miniwob benchmark
for task in ALL_WEBSECARENA_TASKS:
    register_task(task.get_task_id(), task)    