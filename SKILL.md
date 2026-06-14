---
name: fusionclaw
description: "Multi-model deliberation panel: parallel model responses, structured judge analysis, synthesized final answer."
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

Private multi-model deliberation panel. Inspired by OpenRouter Fusion, but running entirely on our infrastructure with Ollama Cloud models.

## When to use

- Complex architectural decisions where no single model has the full picture
- Ambiguous or controversial questions where diverse perspectives reduce blind spots
- Research tasks where consensus and contradiction both matter
- Code review, security analysis, or debugging where multiple angles catch more issues
- User explicitly requests deliberation: "fusion this", "deliberate on X", "panel analysis"
- **NOT for**: simple lookups, straightforward edits, tasks where one model is clearly sufficient

## Architecture

```
User prompt → Conductor (current model)
                ├── Panel (parallel sub-agents, different models)
                │   ├── Panelist 1: GLM-5.1 (deep reasoning)
                │   ├── Panelist 2: Kimi K2.6 (long context, synthesis)
                │   ├── Panelist 3: DeepSeek V4 Pro (technical depth)
                │   └── Panelist 4: Qwen 3.5 / Nemotron (diverse perspective)
                │
                └── Judge (GLM-5.1 or Kimi K2.6)
                       → Structured analysis JSON
                → Final synthesized answer
```

## Presets

| Preset | Panel | Judge | Cost | Use case |
|--------|-------|-------|------|----------|
| **quality** | GLM-5.1, Kimi K2.6, DeepSeek V4 Pro | GLM-5.1 | 4× | Architecture, research, complex analysis |
| **fast** | Kimi K2.7 Code, Qwen 3 Coder | Kimi K2.7 Code | 3× | Code review, debugging |
| **broad** | GLM-5.1, Kimi K2.6, DeepSeek V4 Pro, Nemotron 3 Super | GLM-5.1 | 5× | Maximum diversity, critical decisions |
| **lean** | 2 models from quality panel | GLM-5.1 | 3× | Quick second opinion |

## Models available

| Model | Alias | Strength |
|-------|-------|----------|
| ollama/glm-5.1:cloud | glm5 | Deep reasoning, analysis |
| ollama/kimi-k2.6:cloud | kimi | Long context, synthesis |
| ollama/deepseek-v4-pro:cloud | deepseek | Technical, coding |
| ollama/qwen3.5:cloud | qwen35 | Balanced, diverse |
| ollama/nemotron-3-super:cloud | nemotron | NVIDIA reasoning |
| ollama/kimi-k2.7-code:cloud | kimi27code | Agentic coding |
| ollama/qwen3-coder-next:cloud | qwencoder | Specialized coding |
| ollama/minimax-m2.7:cloud | minimax | Alternative heavy |
| openrouter/openrouter/fusion | fusion | OpenRouter Fusion (external) |

## Workflow

1. **Detect**: User request merits deliberation, or explicit fusion trigger.
2. **Select preset**: Choose panel composition based on task type. Default: quality.
3. **Spawn panel**: Launch `sessions_spawn` for each panelist in parallel with `mode: "run"`, `context: "isolated"`, and the specific model.
4. **Collect**: Wait for all panelist results via `sessions_yield`.
5. **Judge**: Send all panelist responses to the judge model with the structured analysis prompt (see references/judge-prompt.md).
6. **Synthesize**: The conductor (current model) writes the final answer incorporating the judge's analysis.

## Panelist prompt template

```
You are a panelist in a multi-model deliberation. Answer the following question directly and thoroughly.

Question: {QUESTION}

Context: {CONTEXT}

Provide your analysis. Be specific, flag uncertainties, and state your confidence level.
```

## Judge prompt template

See `references/judge-prompt.md` for the full structured analysis prompt.

## Spawning panelists

```yaml
# Example: quality preset, 3 panelists
- task: "FusionClaw panelist. Question: {QUESTION}"
  model: "ollama/glm-5.1:cloud"
  taskName: "fusion-panelist-1"

- task: "FusionClaw panelist. Question: {QUESTION}"  
  model: "ollama/kimi-k2.6:cloud"
  taskName: "fusion-panelist-2"

- task: "FusionClaw panelist. Question: {QUESTION}"
  model: "ollama/deepseek-v4-pro:cloud"
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
- Respect model availability: check Ollama status before panel.
- If a panelist fails, proceed with remaining results (minimum 2).

## Integration with OpenRouter Fusion

For tasks requiring web search or frontier models, include `openrouter/fusion` as a panelist. This delegates the web-augmented deliberation to OpenRouter's infrastructure while keeping orchestration local.