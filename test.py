import gymnasium as gym
import browsergym.core  # register the openended task

# Create an open-ended browsing environment
env = gym.make(
    "browsergym/openended",
    task_kwargs={"start_url": "https://www.google.com/"},
    headless=True
)

obs, info = env.reset()
print("Environment ready!")
print(f"Goal: {info.get('goal', 'Browse the web')}")
env.close()
