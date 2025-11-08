import gymnasium as gym
import runpy
import browsergym.custom_security_tasks  # ensure your tasks are registered

# list registered custom tasks
print("Custom tasks:", [t for t in gym.registry.keys() if "security" in t])

# pick one
task_id = "browsergym/security.prompt_injection.hidden_form"

# create an env with visible browser
env = gym.make(task_id, headless=False)   # headless=False shows Chromium
obs, info = env.reset()

# Some forks return the instruction in info["instruction"], others don’t
print("INFO:", info)

# keep window open for a bit
import time; time.sleep(10)

env.close()
