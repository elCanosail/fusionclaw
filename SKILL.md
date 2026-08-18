---
name: fusionclaw
description: "Multi-model deliberation panel powered by NaN Builders. Parallel model responses, structured judge analysis, synthesized final answer."
metadata: { "openclaw": { "emoji": "🐙" } }
user-invocable: true
allowed-tools:
  - sessions_spawn
  - sessions_yield
  - sessions_list
  - sessions_send
  - lcm_expand_query
  - lcm_grep
  - web_search
  - web_fetch
  - image
  - pdf
---

# FusionClaw

Multi-model deliberation panel powered by [NaN Builders](https://nan.builders). Runs multiple NaN models in parallel on the same prompt, then a judge synthesizes their answers.

## Why NaN Builders

A deliberation panel spawns 3-5 models per question. That's 15-35K tokens per deliberation. Only NaN's 500M tokens/month per model makes this economically viable without counting.

- **500M tokens/month per model** — run panels all day
- **OpenAI-compatible API** — drop-in replacement
- **EU-hosted** — GDPR compliant
- **4+ models available** — genuine diversity for deliberation

## When to use

- Complex architectural decisions where no single model has the full picture
- Ambiguous or controversial questions where diverse perspectives reduce blind spots
- Research tasks where consensus and contradiction both matter
- Code review, security analysis, or debugging where multiple angles catch more issues
- User explicitly requests deliberation: "fusion this", "deliberate on X", "panel analysis"
- **NOT for**: simple lookups, straightforward edits, tasks where one model is clearly sufficient

### When NOT to use

- Simple lookups or factual questions one model can answer
- Straightforward code edits with no architectural implications
- Time-critical responses where parallel deliberation adds latency
- Tasks requiring a single authoritative answer, not diverse perspectives
- When token budget is a concern (use a single model instead)

## Architecture

```
User prompt → Conductor (current model)
                ├── Panel (parallel sub-agents, different NaN models)
                │   ├── Panelist 1: DeepSeek V4 Flash (reasoning)
                │   ├── Panelist 2: Qwen 3.6 (balanced analysis)
                │   ├── Panelist 3: Gemma 4 (diverse perspective)
                │   └── Panelist 4: Mimo V2.5 (lightweight contrast)
                │
                └── Judge (DeepSeek V4 Flash)
                       → Structured analysis JSON
                → Final synthesized answer
```

## Presets

| Preset | Panel | Judge | Use case |
|--------|-------|-------|----------|
| **quality** | DeepSeek V4 Flash, Qwen 3.6, Gemma 4 | DeepSeek V4 Flash | Architecture, research, complex analysis |
| **fast** | DeepSeek V4 Flash, Qwen 3.6 | DeepSeek V4 Flash | Code review, debugging |
| **broad** | DeepSeek V4 Flash, Qwen 3.6, Gemma 4, Mimo V2.5 | DeepSeek V4 Flash | Maximum diversity, critical decisions |
| **lean** | DeepSeek V4 Flash, Qwen 3.6 | DeepSeek V4 Flash | Quick second opinion |

## NaN Models

| Model | Endpoint | Strength |
|-------|----------|----------|
| DeepSeek V4 Flash | `nan/deepseek-v4-flash` | Fast reasoning, technical depth |
| Qwen 3.6 | `nan/qwen3.6` | Balanced, versatile |
| Gemma 4 | `nan/gemma4` | Google-quality, diverse perspective |
| Mimo V2.5 | `nan/mimo-v2.5` | Lightweight, contrasting angle |

## Workflow

1. **Detect**: User request merits deliberation, or explicit fusion trigger.
2. **Select preset**: Choose panel composition based on task type. Default: quality.
3. **Spawn panel**: Launch `sessions_spawn` for each panelist in parallel with `mode: "run"`, `context: "isolated"`, and the specific NaN model.
4. **Collect**: Wait for all panelist results via `sessions_yield`.
5. **Judge**: Send all panelist responses to the judge model with the structured analysis prompt (see judge-prompt.md).
6. **Synthesize**: The conductor (current model) writes the final answer incorporating the judge's analysis.

## Panelist prompt template

```
You are a panelist in a multi-model deliberation. Answer the following question directly and thoroughly.

Question: {QUESTION}

Context: {CONTEXT}

Provide your analysis. Be specific, flag uncertainties, and state your confidence level.
```

## Judge prompt template

See `judge-prompt.md` for the full structured analysis prompt.

## Spawning panelists

```yaml
# Example: quality preset, 3 panelists (all NaN Builders models)
- task: "FusionClaw panelist. Question: {QUESTION}"
  model: "nan/deepseek-v4-flash"
  taskName: "fusion-panelist-1"

- task: "FusionClaw panelist. Question: {QUESTION}"
  model: "nan/qwen3.6"
  taskName: "fusion-panelist-2"

- task: "FusionClaw panelist. Question: {QUESTION}"
  model: "nan/gemma4"
  taskName: "fusion-panelist-3"
```

All spawned with `runtime: "subagent"`, `mode: "run"`, `context: "isolated"`.

## Judge analysis structure

The judge returns JSON with:

```json
{
  "consensus": ["points all or most models agree on"],
  "contradictions": [{"topic": "...", "positions": [...]}],
  "coverage_gaps": ["important aspects no model addressed"],
  "unique_insights": [{"model": "...", "insight": "..."}],
  "confidence_assessment": {"high": [...], "medium": [...], "low": [...]},
  "recommendation": "synthesized best answer"
}
```

## Safety

- Never spawn more than 8 panelists (cost control).
- Always use `mode: "run"` (one-shot, no conversation).
- Sub-agents NEVER push/merge — conductor synthesizes.
- If a panelist fails, proceed with remaining results (minimum 2).
- NaN API availability checked before panel launch.