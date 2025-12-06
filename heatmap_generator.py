"""Generate per-attack blended heatmaps for ASR/STS/DTR ratios.

For each attack, produce a single 3x4 heatmap (models x agents) where
cell color blends the ASR/STS/DTR ratios: more ASR pushes red, more STS
pushes green, more DTR pushes blue. Outputs: `heatmaps/heatmap_<attack>.png`.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


AGENTS = ["Baseline", "Zero-shot", "Few-shot", "Self-reflection"]
MODELS = ["Llama-3.1-8B", "Qwen2.5-7B", "gpt-oss-20b"]
METRICS = ["ASR", "STS", "DTR"]

# data[attack_type][(agent, model)] = [ASR, STS, DTR]
prompt_injection_table = {
    ("Baseline", "Llama-3.1-8B"): [90, 0, 10],
    ("Baseline", "Qwen2.5-7B"): [66, 33, 0],
    ("Baseline", "gpt-oss-20b"): [26, 73, 0],
    ("Zero-shot", "Llama-3.1-8B"): [63, 36, 0],
    ("Zero-shot", "Qwen2.5-7B"): [56, 36, 6],
    ("Zero-shot", "gpt-oss-20b"): [0, 76, 23],
    ("Few-shot", "Llama-3.1-8B"): [43, 46, 10],
    ("Few-shot", "Qwen2.5-7B"): [60, 36, 3],
    ("Few-shot", "gpt-oss-20b"): [0, 96, 3],
    ("Self-reflection", "Llama-3.1-8B"): [26, 46, 26],
    ("Self-reflection", "Qwen2.5-7B"): [60, 13, 26],
    ("Self-reflection", "gpt-oss-20b"): [0, 70, 30],
}

phishing_table = {
    ("Baseline", "Llama-3.1-8B"): [83, 0, 16],
    ("Baseline", "Qwen2.5-7B"): [90, 6, 3],
    ("Baseline", "gpt-oss-20b"): [96, 0, 3],
    ("Zero-shot", "Llama-3.1-8B"): [36, 56, 6],
    ("Zero-shot", "Qwen2.5-7B"): [3, 96, 0],
    ("Zero-shot", "gpt-oss-20b"): [0, 100, 0],
    ("Few-shot", "Llama-3.1-8B"): [20, 63, 16],
    ("Few-shot", "Qwen2.5-7B"): [0, 100, 0],
    ("Few-shot", "gpt-oss-20b"): [0, 100, 0],
    ("Self-reflection", "Llama-3.1-8B"): [20, 63, 16],
    ("Self-reflection", "Qwen2.5-7B"): [0, 100, 0],
    ("Self-reflection", "gpt-oss-20b"): [0, 100, 0],
}

social_engineering_table = {
    ("Baseline", "Llama-3.1-8B"): [90, 10, 0],
    ("Baseline", "Qwen2.5-7B"): [63, 30, 3],
    ("Baseline", "gpt-oss-20b"): [40, 60, 0],
    ("Zero-shot", "Llama-3.1-8B"): [53, 43, 3],
    ("Zero-shot", "Qwen2.5-7B"): [20, 70, 10],
    ("Zero-shot", "gpt-oss-20b"): [6, 93, 0],
    ("Few-shot", "Llama-3.1-8B"): [10, 76, 13],
    ("Few-shot", "Qwen2.5-7B"): [33, 50, 16],
    ("Few-shot", "gpt-oss-20b"): [6, 93, 0],
    ("Self-reflection", "Llama-3.1-8B"): [10, 76, 13],
    ("Self-reflection", "Qwen2.5-7B"): [26, 66, 6],
    ("Self-reflection", "gpt-oss-20b"): [3, 96, 0],
}

clickjacking_table = {
    ("Baseline", "Llama-3.1-8B"): [80, 17, 13],
    ("Baseline", "Qwen2.5-7B"): [100, 0, 0],
    ("Baseline", "gpt-oss-20b"): [0, 100, 0],
    ("Zero-shot", "Llama-3.1-8B"): [73, 20, 7],
    ("Zero-shot", "Qwen2.5-7B"): [96, 4, 0],
    ("Zero-shot", "gpt-oss-20b"): [20, 26, 54],
    ("Few-shot", "Llama-3.1-8B"): [47, 53, 0],
    ("Few-shot", "Qwen2.5-7B"): [0, 100, 0],
    ("Few-shot", "gpt-oss-20b"): [3, 97, 0],
    ("Self-reflection", "Llama-3.1-8B"): [77, 0, 23],
    ("Self-reflection", "Qwen2.5-7B"): [3, 64, 33],
    ("Self-reflection", "gpt-oss-20b"): [0, 100, 0],
}

malicious_redirect_chain_table = {
    ("Baseline", "Llama-3.1-8B"): [60, 37, 3],
    ("Baseline", "Qwen2.5-7B"): [100, 0, 0],
    ("Baseline", "gpt-oss-20b"): [0, 100, 0],
    ("Zero-shot", "Llama-3.1-8B"): [0, 100, 0],
    ("Zero-shot", "Qwen2.5-7B"): [93, 0, 7],
    ("Zero-shot", "gpt-oss-20b"): [0, 100, 0],
    ("Few-shot", "Llama-3.1-8B"): [0, 90, 10],
    ("Few-shot", "Qwen2.5-7B"): [86, 14, 0],
    ("Few-shot", "gpt-oss-20b"): [0, 100, 0],
    ("Self-reflection", "Llama-3.1-8B"): [0, 86, 14],
    ("Self-reflection", "Qwen2.5-7B"): [80, 20, 0],
    ("Self-reflection", "gpt-oss-20b"): [6, 93, 0],
}

drive_by_downloads_table = {
    ("Baseline", "Llama-3.1-8B"): [100, 0, 0],
    ("Baseline", "Qwen2.5-7B"): [100, 0, 0],
    ("Baseline", "gpt-oss-20b"): [100, 0, 0],
    ("Zero-shot", "Llama-3.1-8B"): [33, 67, 0],
    ("Zero-shot", "Qwen2.5-7B"): [0, 100, 0],
    ("Zero-shot", "gpt-oss-20b"): [80, 20, 0],
    ("Few-shot", "Llama-3.1-8B"): [100, 0, 0],
    ("Few-shot", "Qwen2.5-7B"): [67, 33, 0],
    ("Few-shot", "gpt-oss-20b"): [87, 13, 0],
    ("Self-reflection", "Llama-3.1-8B"): [17, 40, 43],
    ("Self-reflection", "Qwen2.5-7B"): [27, 73, 0],
    ("Self-reflection", "gpt-oss-20b"): [77, 23, 0],
}

DATA = {
    "Prompt Injection": prompt_injection_table,
    "Phishing": phishing_table,
    "Social Engineering": social_engineering_table,
    "Clickjacking": clickjacking_table,
    "Redirect-Chains": malicious_redirect_chain_table,
    "Drive-by Downloads": drive_by_downloads_table,
}


def ratios_to_rgb(asr: float, sts: float, dtr: float) -> np.ndarray:
    """Blend ASR/STS/DTR into an RGB color (red, green, blue)."""

    total = asr + sts + dtr
    if total == 0:
        return np.array([0.9, 0.9, 0.9])  # neutral if no data

    r = asr / total
    g = sts / total
    b = dtr / total
    return np.clip(np.array([r, g, b]), 0, 1)


def plot_attack_heatmaps(attack_name: str, table: dict, output_dir: Path) -> None:
    """Save a single blended heatmap (models x agents) for the attack."""

    color_grid = np.zeros((len(MODELS), len(AGENTS), 3))

    for m_idx, model in enumerate(MODELS):
        for a_idx, agent in enumerate(AGENTS):
            asr, sts, dtr = table[(agent, model)]
            color_grid[m_idx, a_idx, :] = ratios_to_rgb(asr, sts, dtr)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(color_grid, aspect="equal")

    ax.set_xticks(range(len(AGENTS)))
    ax.set_xticklabels(AGENTS, rotation=30, ha="right")
    ax.set_yticks(range(len(MODELS)))
    ax.set_yticklabels(MODELS)
    ax.set_title(f"{attack_name} ASR/STS/DTR blend")

    # Simple legend proxies for the color meaning.
    legend_handles = [
        plt.Line2D([0], [0], marker="s", color="w", label="ASR (red)",
                   markerfacecolor="red", markersize=8, linestyle="None"),
        plt.Line2D([0], [0], marker="s", color="w", label="STS (green)",
                   markerfacecolor="green", markersize=8, linestyle="None"),
        plt.Line2D([0], [0], marker="s", color="w", label="DTR (blue)",
                   markerfacecolor="blue", markersize=8, linestyle="None"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        borderaxespad=0,
        frameon=True,
        fontsize=8,
    )

    fig.tight_layout()

    slug = attack_name.lower().replace(" ", "_").replace("-", "_")
    output_path = output_dir / f"heatmap_{slug}.png"
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {output_path}")


def main() -> None:
    output_dir = Path("heatmaps")
    output_dir.mkdir(exist_ok=True)

    for attack_name, table in DATA.items():
        plot_attack_heatmaps(attack_name, table, output_dir)


if __name__ == "__main__":
    main()
