-------------------
## 1x : Exception uncaught by agent or environment in task <task_name>.<br>BadRequestError:<br>(Request ID: Root=1-692d66e5-69d7e7cd20757fa92c5fdac5;dbc425e0-5ee9-4041-91a6-7d91850c79d0)<br><br>Bad request

* websecarena.malicious_redirect_chain seed: 20

Showing Max 3 stack traces:

```bash
2025-12-01 02:58:12,345 - 63800 - root - WARNING - Agent is in goal mode, but multiple user messages are present in the chat. Consider switching to `enable_chat=True`.
2025-12-01 02:58:21,140 - 63800 - root - WARNING - Agent is in goal mode, but multiple user messages are present in the chat. Consider switching to `enable_chat=True`.
2025-12-01 02:58:26,021 - 63800 - root - WARNING - Agent is in goal mode, but multiple user messages are present in the chat. Consider switching to `enable_chat=True`.
2025-12-01 02:58:30,688 - 63800 - root - WARNING - Agent is in goal mode, but multiple user messages are present in the chat. Consider switching to `enable_chat=True`.
2025-12-01 02:58:39,840 - 63800 - root - WARNING - Agent is in goal mode, but multiple user messages are present in the chat. Consider switching to `enable_chat=True`.
2025-12-01 02:58:42,104 - 63800 - root - WARNING - Failed to get a response from the server: 
(Request ID: Root=1-692d66d0-58af1b643a9df1564ff0fce5;5053071e-67f1-4d67-9f47-5fe32841cfcf)

Bad request:
Retrying... (1/4)
...
...truncated middle of the log
...

Bad request:
Retrying... (3/4)
2025-12-01 02:59:03,271 - 63800 - agentlab.experiments.loop - WARNING - Exception uncaught by agent or environment in task websecarena.malicious_redirect_chain.
BadRequestError:
(Request ID: Root=1-692d66e5-69d7e7cd20757fa92c5fdac5;dbc425e0-5ee9-4041-91a6-7d91850c79d0)

Bad request:
Traceback (most recent call last):
  File "C:\Adarsh Home\Projects\Benchmarking_main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\.venv\Lib\site-packages\huggingface_hub\utils\_http.py", line 402, in hf_raise_for_status
    response.raise_for_status()
  File "C:\Adarsh Home\Projects\Benchmarking_main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\.venv\Lib\site-packages\requests\models.py", line 1026, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 400 Client Error: Bad Request for url: https://router.huggingface.co/novita/v3/openai/chat/completions

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Adarsh Home\Projects\Benchmarking_main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\agentlab\src\agentlab\experiments\loop.py", line 439, in run
    action = step_info.from_action(agent)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Adarsh Home\Projects\Benchmarking_main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\agentlab\src\agentlab\experiments\loop.py", line 223, in from_action
    self.action, self.agent_info = agent.get_action(self.obs.copy())
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Adarsh Home\Projects\Benchmarking_main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\agentlab\src\agentlab\llm\tracking.py", line 84, in wrapper
    action, agent_info = get_action(self, obs)
                         ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Adarsh Home\Projects\Benchmarking_main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\agentlab\src\agentlab\agents\generic_agent\generic_agent.py", line 135, in get_action
    ans_dict = retry(
               ^^^^^^
  File "C:\Adarsh Home\Projects\Benchmarking_main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\agentlab\src\agentlab\llm\llm_utils.py", line 86, in retry
    answer = chat(messages)
             ^^^^^^^^^^^^^^
  File "C:\Adarsh Home\Projects\Benchmarking_main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\agentlab\src\agentlab\llm\huggingface_utils.py", line 130, in __call__
    raise e
  File "C:\Adarsh Home\Projects\Benchmarking_main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\agentlab\src\agentlab\llm\huggingface_utils.py", line 119, in __call__
    answer = self.llm(messages.to_dicts(), temperature=temperature)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Adarsh Home\Projects\Benchmarking_main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\.venv\Lib\site-packages\huggingface_hub\inference\_client.py", line 915, in chat_completion
    data = self._inner_post(request_parameters, stream=stream)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Adarsh Home\Projects\Benchmarking_main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\.venv\Lib\site-packages\huggingface_hub\inference\_client.py", line 275, in _inner_post
    hf_raise_for_status(response)
  File "C:\Adarsh Home\Projects\Benchmarking_main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\Benchmarking-Privacy-Aware-Autonomous-AI-Agents-main\.venv\Lib\site-packages\huggingface_hub\utils\_http.py", line 458, in hf_raise_for_status
    raise _format(BadRequestError, message, response) from e
huggingface_hub.errors.BadRequestError: (Request ID: Root=1-692d66e5-69d7e7cd20757fa92c5fdac5;dbc425e0-5ee9-4041-91a6-7d91850c79d0)

Bad request:


```