from browsergym.core.registration import register_task

from tasks.custom_security_tasks import AdversarialEmotionalManipulationTask, AdversarialFakeAuthorityTask, AdversarialMisinformationTask, MaliciousClickjackTask, MaliciousPopupRedirectTask, MaliciousRedirectChainTask, PhishingDataHarvestingFormTask, PhishingFakePasswordResetTask, PhishingSuspiciousLoginTask, PromptInjectionHTMLCommentTask, PromptInjectionHiddenFormTask, PromptInjectionScriptTask, SampleTask

register_task(id=SampleTask.get_task_id(), task_class=SampleTask)
register_task("security.prompt_injection.hidden_form", PromptInjectionHiddenFormTask)
register_task("security.prompt_injection.html_comment", PromptInjectionHTMLCommentTask)
register_task("security.prompt_injection.script", PromptInjectionScriptTask)
register_task("security.phishing.suspicious_login", PhishingSuspiciousLoginTask)
register_task("security.phishing.fake_password_reset", PhishingFakePasswordResetTask)
register_task("security.phishing.data_harvesting_form", PhishingDataHarvestingFormTask)
register_task("security.malicious.clickjack", MaliciousClickjackTask)
register_task("security.malicious.redirect_chain", MaliciousRedirectChainTask)
register_task("security.malicious.popup_redirect", MaliciousPopupRedirectTask)
register_task("security.adversarial.emotional_manipulation", AdversarialEmotionalManipulationTask)
register_task("security.adversarial.fake_authority", AdversarialFakeAuthorityTask)
register_task("security.adversarial.misinformation", AdversarialMisinformationTask)
