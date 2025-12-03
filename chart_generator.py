import matplotlib.pyplot as plt
import numpy as np

agents = ["Baseline", "Zero-shot", "Few-shot", "Self-reflection"]
models = ["Llama-3.1-8B", "Qwen2.5-7B", "gpt-oss-20b"]
attack_types = [
    "Prompt Injection",
    "Social Engineering",
    "Phishing",
    "Clickjacking",
    "Redirect-Chains",
    "Drive-by Downloads",
]

# Example data structure:
# data[attack_type][(agent, model)] = [ASR, STS, DTR]  (percentages from WebSecArena_report.md)
prompt_injection_table = {
    ("Baseline", "Llama-3.1-8B"):      [90, 0, 10],
    ("Baseline", "Qwen2.5-7B"):        [66, 33, 0],
    ("Baseline", "gpt-oss-20b"):       [26, 73, 0],
    ("Zero-shot", "Llama-3.1-8B"):     [63, 36, 0],
    ("Zero-shot", "Qwen2.5-7B"):       [56, 36, 6],
    ("Zero-shot", "gpt-oss-20b"):      [0, 76, 23],
    ("Few-shot", "Llama-3.1-8B"):      [43, 46, 10],
    ("Few-shot", "Qwen2.5-7B"):        [60, 36, 3],
    ("Few-shot", "gpt-oss-20b"):       [0, 96, 3],
    ("Self-reflection", "Llama-3.1-8B"): [26, 46, 26],
    ("Self-reflection", "Qwen2.5-7B"):   [60, 13, 26],
    ("Self-reflection", "gpt-oss-20b"):  [0, 70, 30],
}

phishing_table = {
    ("Baseline", "Llama-3.1-8B"):      [83, 0, 16],
    ("Baseline", "Qwen2.5-7B"):        [90, 6, 3],
    ("Baseline", "gpt-oss-20b"):       [96, 0, 3],
    ("Zero-shot", "Llama-3.1-8B"):     [36, 56, 6],
    ("Zero-shot", "Qwen2.5-7B"):       [3, 96, 0],
    ("Zero-shot", "gpt-oss-20b"):      [0, 100, 0],
    ("Few-shot", "Llama-3.1-8B"):      [20, 63, 16],
    ("Few-shot", "Qwen2.5-7B"):        [0, 100, 0],
    ("Few-shot", "gpt-oss-20b"):       [0, 100, 0],
    ("Self-reflection", "Llama-3.1-8B"): [20, 63, 16],
    ("Self-reflection", "Qwen2.5-7B"):   [0, 100, 0],
    ("Self-reflection", "gpt-oss-20b"):  [0, 100, 0],
}

social_engineering_table = {
    ("Baseline", "Llama-3.1-8B"):      [90, 10, 0],
    ("Baseline", "Qwen2.5-7B"):        [63, 30, 3],
    ("Baseline", "gpt-oss-20b"):       [40, 60, 0],
    ("Zero-shot", "Llama-3.1-8B"):     [53, 43, 3],
    ("Zero-shot", "Qwen2.5-7B"):       [20, 70, 10],
    ("Zero-shot", "gpt-oss-20b"):      [6, 93, 0],
    ("Few-shot", "Llama-3.1-8B"):      [10, 76, 13],
    ("Few-shot", "Qwen2.5-7B"):        [33, 50, 16],
    ("Few-shot", "gpt-oss-20b"):       [6, 93, 0],
    ("Self-reflection", "Llama-3.1-8B"): [10, 76, 13],
    ("Self-reflection", "Qwen2.5-7B"):   [26, 66, 6],
    ("Self-reflection", "gpt-oss-20b"):  [3, 96, 0],
}

clickjacking_table = {
    ("Baseline", "Llama-3.1-8B"):      [80, 17, 13],
    ("Baseline", "Qwen2.5-7B"):        [100, 0, 0],
    ("Baseline", "gpt-oss-20b"):       [0, 100, 0],
    ("Zero-shot", "Llama-3.1-8B"):     [73, 20, 7],
    ("Zero-shot", "Qwen2.5-7B"):       [96, 4, 0],
    ("Zero-shot", "gpt-oss-20b"):      [20, 26, 54],
    ("Few-shot", "Llama-3.1-8B"):      [47, 53, 0],
    ("Few-shot", "Qwen2.5-7B"):        [0, 100, 0],
    ("Few-shot", "gpt-oss-20b"):       [3, 97, 0],
    ("Self-reflection", "Llama-3.1-8B"): [77, 0, 23],
    ("Self-reflection", "Qwen2.5-7B"):   [3, 64, 33],
    ("Self-reflection", "gpt-oss-20b"):  [0, 100, 0],
}

malicious_redirect_chain_table = {
    ("Baseline", "Llama-3.1-8B"):      [60, 37, 3],
    ("Baseline", "Qwen2.5-7B"):        [100, 0, 0],
    ("Baseline", "gpt-oss-20b"):       [0, 100, 0],
    ("Zero-shot", "Llama-3.1-8B"):     [0, 100, 0],
    ("Zero-shot", "Qwen2.5-7B"):       [93, 0, 7],
    ("Zero-shot", "gpt-oss-20b"):      [0, 100, 0],
    ("Few-shot", "Llama-3.1-8B"):      [0, 90, 10],
    ("Few-shot", "Qwen2.5-7B"):        [86, 14, 0],
    ("Few-shot", "gpt-oss-20b"):       [0, 100, 0],
    ("Self-reflection", "Llama-3.1-8B"): [0, 86, 14],
    ("Self-reflection", "Qwen2.5-7B"):   [80, 20, 0],
    ("Self-reflection", "gpt-oss-20b"):  [6, 93, 0],
}

drive_by_downloads_table = {
    ("Baseline", "Llama-3.1-8B"):      [100, 0, 0],
    ("Baseline", "Qwen2.5-7B"):        [100, 0, 0],
    ("Baseline", "gpt-oss-20b"):       [100, 0, 0],
    ("Zero-shot", "Llama-3.1-8B"):     [33, 67, 0],
    ("Zero-shot", "Qwen2.5-7B"):       [0, 100, 0],
    ("Zero-shot", "gpt-oss-20b"):      [80, 20, 0],
    ("Few-shot", "Llama-3.1-8B"):      [100, 0, 0],
    ("Few-shot", "Qwen2.5-7B"):        [67, 33, 0],
    ("Few-shot", "gpt-oss-20b"):       [87, 13, 0],
    ("Self-reflection", "Llama-3.1-8B"): [17, 40, 43],
    ("Self-reflection", "Qwen2.5-7B"):   [27, 73, 0],
    ("Self-reflection", "gpt-oss-20b"):  [77, 23, 0],
}

data = {
    "Prompt Injection": prompt_injection_table,
    "Phishing": phishing_table,
    "Social Engineering": social_engineering_table,
    "Clickjacking": clickjacking_table,
    "Redirect-Chains": malicious_redirect_chain_table,
    "Drive-by Downloads": drive_by_downloads_table,
}

# Create an (attacks x models) grid of subplots
fig, axs = plt.subplots(
    nrows=len(attack_types),
    ncols=len(models),
    figsize=(12, 18),
    sharey=True
)
fig.subplots_adjust(hspace=0.5, top=0.95, bottom=0.05)  # increase spacing between rows


for i, attack in enumerate(attack_types):
    for j, model in enumerate(models):
        ax = axs[i, j]

        asr_vals, sts_vals, dtr_vals = [], [], []
        for agent in agents:
            asr, sts, dtr = data[attack][(agent, model)]
            total = asr + sts + dtr
            asr_vals.append(asr / total)
            sts_vals.append(sts / total)
            dtr_vals.append(dtr / total)

        x = np.arange(len(agents))

        # Stacked bars (ASR red, STS green, DTR gray)
        ax.bar(x, asr_vals, label="ASR", color="red")
        ax.bar(x, sts_vals, bottom=asr_vals, label="STS", color="green")
        ax.bar(
            x,
            dtr_vals,
            bottom=np.array(asr_vals) + np.array(sts_vals),
            label="DTR",
            color="gray",
        )

        # Titles and labels
        if i == 0:
            ax.set_title(model)
        if j == 0:
            ax.set_ylabel(f"{attack}")

        ax.set_xticks(x)
        ax.set_xticklabels(agents, rotation=30, ha="right")
        ax.set_ylim(0, 1)

# Legend in the top-right of the full figure
handles, labels = axs[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper right", title="Outcome")

fig.suptitle("WebSecArena Results")
# plt.tight_layout(rect=[0, 0, 0.93, 0.94])
# plt.tight_layout()

fig.text(
    0.5, -0.02,
    "ASR/STS/DTR proportions across attacks, models, and agent types (WebSecArena)",
    ha="center",
    va="top",
    fontsize=9,
)

out_path = "websecarena_charts.png"
plt.savefig(out_path, dpi=300, bbox_inches="tight")
plt.show()
