#!/usr/bin/env python3
"""Read-only RLM sidecar for 1C deep research."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from rlm import RLM

MODE_ITERATIONS = {"focused": 12, "system": 24, "exhaustive": 30}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run RLM over a bounded 1C research corpus")
    p.add_argument("--question", required=True)
    p.add_argument("--corpus", required=True, type=Path)
    p.add_argument("--mode", choices=MODE_ITERATIONS, default="system")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args()


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def load_project_env() -> None:
    """Load RLM_* defaults from the nearest .dev.env without overriding process env."""
    for base in [Path.cwd(), *Path.cwd().parents]:
        candidate = base / ".dev.env"
        if not candidate.is_file():
            continue
        for raw in candidate.read_text(encoding="utf-8-sig").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if key.startswith("RLM_") and key not in os.environ:
                os.environ[key] = value.strip()
        return


def main() -> int:
    load_project_env()
    args = parse_args()
    if env("RLM_ENABLED", "manual").lower() == "off":
        raise SystemExit("RLM is disabled by RLM_ENABLED=off")

    corpus = args.corpus.read_text(encoding="utf-8")
    backend = env("RLM_BACKEND", "openai")
    model = env("RLM_MODEL")
    if not model:
        raise SystemExit("RLM_MODEL is empty; configure the model before running deep research")
    environment = env("RLM_ENVIRONMENT", "docker")
    backend_kwargs = {"model_name": model}
    base_url = env("RLM_BASE_URL")
    if base_url:
        backend_kwargs["base_url"] = base_url

    rlm = RLM(
        backend=backend,
        backend_kwargs=backend_kwargs,
        environment=environment,
        max_depth=1,
        max_iterations=MODE_ITERATIONS[args.mode],
        verbose=args.verbose,
    )

    prompt = {
        "question": args.question,
        "mode": args.mode,
        "instructions": (
            "Analyze the supplied 1C research corpus. Decompose it programmatically, "
            "use sub-LM calls when useful, distinguish evidence from inference, and return "
            "a compact architecture/research synthesis. Never propose or execute file mutations."
        ),
        "corpus": corpus,
    }
    result = rlm.completion(prompt)
    print(result.response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())