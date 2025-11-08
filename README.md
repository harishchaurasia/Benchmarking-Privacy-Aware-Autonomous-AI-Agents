# Benchmarking Privacy-Aware Autonomous AI Agents  
**Branch:** `adarsh`  
**Author:** Adarsh Mohan  

---

## 📘 Overview

This branch sets up a **controlled testbed** to study how **large language model (LLM)–based web agents** behave when exposed to **malicious or privacy-sensitive webpages** using **BrowserGym** and **Groq’s Llama-3.3-70B model**.

Unlike standard benchmarking, the goal here is **not to achieve a correct answer**, but to **observe behavior** — how the agent reacts when webpages attempt risky actions such as hidden downloads, data exfiltration, or deceptive UI prompts.

This branch is currently focused on:

> 🧩 **Task 5 – Untrusted File Handling & Drive-By Downloads**  
> Evaluating how an autonomous agent behaves when a webpage tries to trigger unwanted file downloads or access local resources.

---

## 🧠 What Has Been Done

1. **Integrated a Groq-powered LLM agent** (`run_groq_agent.py`) with BrowserGym.  
   The model receives the web page content and task goal and responds with text or code actions.

2. **Vendored (local) copies of BrowserGym and AgentLab** are now included — no submodules.  
   This makes the workspace self-contained and reproducible.

3. **Added custom security test tasks** under `browsergym/custom_security_tasks.py`:
   - `security.files.auto_download`  
     → Simulates a “drive-by download” of a file.  
   - `security.files.blob_trap`  
     → Simulates a “fake invoice PDF” blob that prompts unsafe interaction.

4. **Created local test webpages** in the `assets/` directory:
   - `assets/auto_download.html`  
   - `assets/blob_trap.html`  
   These represent malicious pages used by the above BrowserGym tasks.

5. **Implemented and tested the Groq runner**:
   ```bash
   python run_groq_agent.py browsergym/security.files.auto_download
   python run_groq_agent.py browsergym/security.files.blob_trap


## ⚙️ How to Set It Up on Your Machine

### 1️⃣ Clone the repository and switch to the `adarsh` branch
```bash
git clone https://github.com/harishchaurasia/Benchmarking-Privacy-Aware-Autonomous-AI-Agents.git
cd Benchmarking-Privacy-Aware-Autonomous-AI-Agents
git checkout adarsh
# If you already have the shared environment
source ~/envs/bgym/bin/activate

# Or create your own
python3 -m venv bgym
source bgym/bin/activate


#install dependencies
pip install -r browsergym/requirements.txt
pip install -r agentlab/requirements.txt
pip install python-dotenv groq gymnasium playwright


#create a .env file at project root
GROQ_API_KEY=sk-your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile

# run  the agents on the task
python run_groq_agent.py browsergym/security.files.auto_download
