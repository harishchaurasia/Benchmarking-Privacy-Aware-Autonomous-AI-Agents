import gymnasium as gym
import time
import tasks  # will register the gym environment

# Create the BrowserGym env for the registered task
env_id = "browsergym/security.prompt_injection.hidden_form"
print(f"Making env: {env_id}")
env = gym.make(env_id)

# Reset environment (returns initial observation and info)
obs, info = env.reset()
print("Env reset. Goal / initial messages (truncated):")
# 'goal' is part of the observation or info depending on your BrowserGym build; print a short excerpt:
print(obs.get("goal_object", obs.get("goal", "NO_GOAL_IN_OBS")))

terminated = False
truncated = False

# Step 1: Fill the feedback textarea with a safe string.
# Using BrowserGym's raw-python action: the string is executed with access to a Playwright `page` object.
fill_action = (
    "page.evaluate(\"document.getElementById('feedback_text').value = 'This is safe feedback provided by the agent.'\")"
)
obs, reward, terminated, truncated, info = env.step(fill_action)
print("Filled textarea -> reward:", reward, "terminated:", terminated, "truncated:", truncated)
if info.get("last_action_error"):
    print("Action error:", info["last_action_error"])

# small pause to let the page update (not strictly required in deterministic envs)
time.sleep(0.5)

# Step 2: Click Submit
click_action = "page.evaluate(\"document.getElementById('submit_btn').click()\")"
obs, reward, terminated, truncated, info = env.step(click_action)
print("Clicked submit -> reward:", reward, "terminated:", terminated, "truncated:", truncated)
if info.get("last_action_error"):
    print("Action error:", info["last_action_error"])

# Continue stepping with noop until env signals done (validate() might require a step to mark done)
while not (terminated or truncated):
    noop_action = "noop(500)"  # noop is one of the high-level primitives; it's accepted by default action mapping
    obs, reward, terminated, truncated, info = env.step(noop_action)
    print("noop step -> reward:", reward, "terminated:", terminated, "truncated:", truncated)
    if info.get("last_action_error"):
        print("Action error:", info["last_action_error"])
    time.sleep(0.2)

# Episode finished — print final info / chat messages for debugging
print("\n=== Episode finished ===")
print("Final reward:", reward)
# Depending on BrowserGym version, validation message may be in info or in the observation
if "task_message" in info:
    print("Task message:", info["task_message"])
# Observations often contain chat_messages or goal_object
if obs:
    if "chat_messages" in obs:
        print("Chat messages (last 10):")
        for m in obs["chat_messages"][-10:]:
            print(m)
    else:
        print("Final observation keys:", list(obs.keys()))

# Close env
env.close()