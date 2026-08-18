---
name: rlm-deep-research
description: Run optional Recursive Language Model deep research over a bounded read-only 1C corpus. Used by 1c-deep-research for system-scale analysis; never for ordinary local exploration or source mutation.
---

# RLM Deep Research

Use this skill only from `1c-deep-research` or when the user explicitly requests RLM / deep recursive research.

The official implementation is `alexzhang13/rlm`, installed from PyPI as `rlms` (Python 3.11+). The portable wrapper ships inside this skill at `content/skills/rlm-deep-research/scripts/rlm_1c.py` (installed clients use the equivalent `.cursor/skills/...`, `.claude/skills/...`, etc. path).

## Preconditions

1. The research question and scope are already bounded through MCP-first discovery.
2. Input is read-only project material; secrets, credentials, `.dev.env`, binary infobases, and unrelated files are excluded.
3. `RLM_ENABLED` resolves to `manual` or `auto`; `off` forbids invocation.
4. Python 3.11+ with `rlms` is available outside the 1C runtime. Docker is preferred for REPL isolation.

If any runtime prerequisite is missing, do not install software automatically. Report the missing prerequisite and fall back to `1c-explorer` + parent synthesis.
## Invocation contract

Create a UTF-8 corpus file containing the research question, scope manifest, and selected evidence. Prefer MCP-derived summaries plus only the necessary BSL/XML excerpts rather than an indiscriminate repository dump.

Run:

```text
python <active-skill-root>/rlm-deep-research/scripts/rlm_1c.py --question "<question>" --corpus <path> --mode focused|system|exhaustive
```

The wrapper prints the final RLM response to stdout. The parent/subagent must verify load-bearing 1C facts through deterministic MCP tools before treating them as confirmed.

## Modes

- `focused`: max 12 REPL iterations; one large mechanism or bounded cross-module question.
- `system`: max 24 iterations; subsystem / multi-extension analysis. Default for automatic routing.
- `exhaustive`: max 30 iterations; project-wide audit. Use only on explicit scope that justifies it.

## Security

The official RLM exposes the input as a `context` variable and lets the root LM execute Python to inspect/decompose it and call sub-LMs. Keep the sidecar read-only. Never pass write-capable MCP tools or secrets into RLM custom tools. Prefer `RLM_ENVIRONMENT=docker`; `local` is an explicit trusted-development fallback only.