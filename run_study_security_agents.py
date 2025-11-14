#!/usr/bin/env python3
"""
Run both security-aware agents on the full WebSecArena benchmark.

Usage examples:
  # Default: run both prompt-security agents, 3 repeats, 1 job
  python run_study_security_agents.py

  # Add the proper SecurityGuard wrapper as well
  python run_study_security_agents.py --include-guard

  # More repeats, custom results folder, parallel jobs via Ray
  python run_study_security_agents.py --repeats 5 --n-jobs 2 --exp-root ./studies/websecarena_security

Notes:
- This expects the two prompt-based agents to be exported from:
    agentlab.agents.generic_agent: 
      AGENT_SECURITY_PROMPT_MINIMAL, AGENT_SECURITY_PROMPT_STRICT
- If you also created the proper security agent wrapper:
    agentlab.agents.security_agent:
      AGENT_SECURITY_GUARD
"""

from __future__ import annotations
import argparse
import logging
from pathlib import Path
import sys

# --- Optional local path bootstrap (useful if you didn't pip-install the packages) ---
ROOT = Path(__file__).resolve().parent
for p in [
    ROOT / "agentlab" / "src",
    ROOT / "browsergym" / "browsergym" / "experiments" / "src",
    ROOT / "browsergym" / "websecarena" / "src",
]:
    if str(p) not in sys.path and p.exists():
        sys.path.insert(0, str(p))

# Ensure WebSecArena envs are registered with Gym
import browsergym.websecarena  # noqa: F401

from agentlab.experiments.study import make_study
from agentlab.agents.generic_agent import (
    AGENT_SECURITY_PROMPT_MINIMAL,
    AGENT_SECURITY_PROMPT_STRICT,
)

# Optional: proper guard agent (if you added it)
try:
    from agentlab.agents.security_agent import AGENT_SECURITY_GUARD  # type: ignore
except Exception:
    AGENT_SECURITY_GUARD = None  # gracefully continue if not available

# For custom repeats (otherwise make_study("websecarena") uses defaults)
try:
    from bgym import DEFAULT_BENCHMARKS
except Exception:
    DEFAULT_BENCHMARKS = None  # fallback to string benchmark


def build_benchmark(repeats: int | None):
    """Return a Benchmark object (with repeats) if possible, else the string name."""
    if repeats and repeats > 0 and DEFAULT_BENCHMARKS is not None:
        # In your repo, DEFAULT_BENCHMARKS["websecarena"](n_repeats=R) expands to the 2 tasks:
        #   websecarena.prompt_injection_hidden_form
        #   websecarena.prompt_injection_html_comment
        return DEFAULT_BENCHMARKS["websecarena"](n_repeats=repeats)
    return "websecarena"


def parse_args():
    p = argparse.ArgumentParser(description="Run security agents on WebSecArena benchmark.")
    p.add_argument("--repeats", type=int, default=3,
                   help="How many repeats per task (default: 3).")
    p.add_argument("--n-jobs", type=int, default=1,
                   help="Number of parallel jobs (default: 1).")
    p.add_argument("--parallel-backend", type=str, default="ray",
                   choices=["ray", "sequential"],
                   help="Parallel backend to use (default: ray).")
    p.add_argument("--exp-root", type=str, default="./studies/websecarena_security",
                   help="Directory where the study folder will be created.")
    p.add_argument("--suffix", type=str, default="",
                   help="Optional suffix appended to study name.")
    p.add_argument("--max-steps", type=int, default=None,
                   help="Override max steps per episode (optional).")
    p.add_argument("--include-guard", action="store_true",
                   help="Also run the proper SecurityGuard agent (if available).")
    p.add_argument("--reproducible", action="store_true",
                   help="Enable stricter reproducibility (temperature=0 where supported).")
    return p.parse_args()


def main():
    args = parse_args()
    logging.getLogger().setLevel(logging.INFO)

    # Collect agents (both prompt-engineered security agents)
    agent_args = [
        AGENT_SECURITY_PROMPT_MINIMAL,
        AGENT_SECURITY_PROMPT_STRICT,
    ]
    # Optional proper wrapper agent
    if args.include_guard and AGENT_SECURITY_GUARD is not None:
        agent_args.append(AGENT_SECURITY_GUARD)

    # Give them nice, explicit names (helps in Xray and CSVs)
    # If your AgentArgs already set agent_name, this just overwrites with clearer labels.
    try:
        agent_args[0].agent_name = "GenericAgent-SecMinimal"
        agent_args[1].agent_name = "GenericAgent-SecStrict"
        if args.include_guard and AGENT_SECURITY_GUARD is not None:
            agent_args[2].agent_name = "SecurityGuard"
    except Exception:
        pass  # Not fatal if dataclass prevents setting (unlikely)

    # Build the benchmark (entire WebSecArena as defined in your repo)
    benchmark = build_benchmark(args.repeats)

    # Create the study
    study = make_study(
        agent_args=agent_args,
        benchmark=benchmark,
        suffix=args.suffix,
        logging_level=logging.INFO,
        logging_level_stdout=logging.INFO,
    )

    # Optional: override max steps per episode
    if args.max_steps is not None:
        study.override_max_steps(args.max_steps)

    # Some AgentLab versions accept exp_root directly in run(); others use make_dir/save.
    # We call run() with exp_root if supported, else fall back to make_dir/save.
    try:
        # Preferred (matches your existing run_study_hidden_form.py style)
        study.run(n_jobs=args.n_jobs, parallel_backend=args.parallel_backend, exp_root=args.exp_root)
    except TypeError:
        # Fallback for older signatures
        try:
            study.make_dir(exp_root=args.exp_root)
        except Exception:
            pass
        study.run(n_jobs=args.n_jobs, parallel_backend=args.parallel_backend)
        try:
            study.save(exp_root=args.exp_root)
        except Exception:
            pass

    # Summarize & save CSVs/markdown into the study folder
    try:
        result_df, summary_df, error_report = study.get_results(also_save=True)
        print("\n=== Summary (per agent & task) ===")
        print(summary_df)
        print("\n=== Error Report (truncated) ===")
        print(error_report[:2000])
    except Exception as e:
        print("Warning: could not summarize results:", e)

    print(f"\nDone. Study saved under: {study.dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
