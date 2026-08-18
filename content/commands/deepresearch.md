---
description: Force a read-only system-scale 1C Deep Research run through the 1c-deep-research subagent and optional RLM sidecar
argumentHint: "[focused|system|exhaustive] <research question>"
---

# /deepresearch — system-scale 1C research

Use when the user explicitly wants a deep recursive investigation rather than ordinary bounded exploration.

Parse the first argument as mode: `focused`, `system`, or `exhaustive`. If omitted, use `system`. The rest is the research question.

## Flow

1. Load `content/rules/subagents.md` and `content/agents/deep-research.md`.
2. Keep the task read-only. Do not implement or mutate project sources.
3. Run MCP-first scoping and identify the minimum relevant corpus.
4. Launch `1c-deep-research` with the question, mode, scope, and available MCP evidence.
5. The subagent loads `rlm-deep-research`; if RLM prerequisites are unavailable, it must state degraded mode and fall back to bounded exploration plus synthesis.
6. Verify load-bearing 1C facts deterministically before presenting them as confirmed.
7. Return the compressed Deep Research report and recommend the next agent only when further work is actually needed.

`/deepresearch` is an explicit override: it may run even when automatic triage would have selected `1c-explorer`, but it does not relax any MCP-first, security, or read-only boundary.