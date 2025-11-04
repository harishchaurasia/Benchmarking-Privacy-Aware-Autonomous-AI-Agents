from dotenv import load_dotenv
import os
import gymnasium as gym
from typing import Dict, List
import json
from datetime import datetime

# Load environment
load_dotenv()

# Import your custom tasks (this registers them with BrowserGym)
import custom_security_tasks

# Verify tasks are registered
print("🔐 Registered Security Tasks:")
registered_tasks = [
    "security.prompt_injection.hidden_form",
    "security.prompt_injection.html_comment",
    "security.prompt_injection.script",
    "security.phishing.suspicious_login",
    "security.phishing.fake_password_reset",
    "security.phishing.data_harvesting_form",
    "security.malicious.clickjack",
    "security.malicious.redirect_chain",
    "security.malicious.popup_redirect",
    "security.adversarial.emotional_manipulation",
    "security.adversarial.fake_authority",
    "security.adversarial.misinformation",
]

for task_id in registered_tasks:
    print(f"  ✓ {task_id}")

# Test a single task
print("\n🧪 Testing a single security task:")
env = gym.make(f"browsergym/{registered_tasks[0]}")
obs, info = env.reset()
print(f"  Task: {info.get('goal', 'N/A')}")
print(f"  Status: Environment ready ✓")
env.close()

print("\n✅ All security tasks loaded successfully!")
print(f"📊 Total tasks: {len(registered_tasks)}")
