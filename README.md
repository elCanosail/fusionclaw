# FusionClaw 🐙

Private multi-model deliberation panel for OpenClaw. Inspired by [OpenRouter Fusion](https://openrouter.ai/docs/guides/routing/routers/fusion-router), running entirely on our infrastructure with Ollama Cloud models.

## Why

One model has biases. A panel catches blind spots, surfaces contradictions, and builds consensus through diversity. OpenRouter Fusion does this with frontier models — we do it for free with our own Ollama Cloud fleet.

## How It Works

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

1. **Conductor** decides if the task merits deliberation
2. **Panelists** answer the same prompt in parallel, each with a different model
3. **Judge** receives all panelist responses and produces structured analysis: consensus, contradictions, gaps, unique insights, confidence levels
4. **Conductor** synthesizes the final answer from the judge's analysis

## Presets

| Preset | Panel | Judge | Cost | Best for |
|--------|-------|-------|------|----------|
| **quality** | GLM-5.1, Kimi K2.6, DeepSeek V4 Pro | GLM-5.1 | 4× | Architecture, research, complex analysis |
| **fast** | Kimi K2.7 Code, Qwen 3 Coder | Kimi K2.7 Code | 3× | Code review, debugging |
| **broad** | GLM-5.1, Kimi K2.6, DeepSeek V4 Pro, Nemotron 3 Super | GLM-5.1 | 5× | Maximum diversity, critical decisions |
| **lean** | 2 models from quality panel | GLM-5.1 | 3× | Quick second opinion |

See [presets.md](./presets.md) for full details and model aliases.

## Available Models

| Model | Ollama Alias | Strength |
|-------|-------------|----------|
| GLM-5.1 | `ollama/glm-5.1:cloud` | Deep reasoning, analysis |
| Kimi K2.6 | `ollama/kimi-k2.6:cloud` | Long context, synthesis |
| Kimi K2.7 Code | `ollama/kimi-k2.7-code:cloud` | Agentic coding |
| DeepSeek V4 Pro | `ollama/deepseek-v4-pro:cloud` | Technical depth |
| Qwen 3.5 | `ollama/qwen3.5:cloud` | Balanced, diverse |
| Nemotron 3 Super | `ollama/nemotron-3-super:cloud` | NVIDIA reasoning |
| MiniMax M2.7 | `ollama/minimax-m2.7:cloud` | Alternative heavy |
| DeepSeek V4 Flash | `ollama/deepseek-v4-flash:cloud` | Fast, good reasoning |

## Judge Analysis Output

The judge returns structured JSON:

```json
{
  "consensus": ["Points all/most models agree on"],
  "contradictions": [{"topic": "...", "positions": [...]}],
  "coverage_gaps": ["Important aspects no model addressed"],
  "unique_insights": [{"model": "...", "insight": "..."}],
  "confidence_assessment": {
    "high": ["Strong multi-model agreement"],
    "medium": ["Partial agreement"],
    "low": ["Little agreement or weak evidence"]
  },
  "recommendation": "Synthesized best answer with uncertainty flags"
}
```

See [judge-prompt.md](./judge-prompt.md) for the full judge prompt template.

## Usage in OpenClaw

FusionClaw is an OpenClaw skill. Trigger it by:
- Saying "fusion this" or "deliberate on X"
- Asking for a panel analysis
- When Elcano detects a task merits deliberation (complex architecture, ambiguous decisions, security review)

The skill is at `~/.openclaw/workspace/skills/fusionclaw/SKILL.md`.

## Integration with OpenRouter Fusion

For tasks requiring web search or frontier models, `openrouter/fusion` can be included as a panelist. This delegates web-augmented deliberation to OpenRouter while keeping orchestration local.

## Safety

- Maximum 8 panelists (cost control)
- All sub-agents use `mode: "run"` (one-shot, no conversation)
- Sub-agents never push/merge — conductor synthesizes
- If a panelist fails, proceed with remaining results (minimum 2)
- Ollama availability checked before panel launch

## Cost

All Ollama Cloud models are free (only infrastructure cost). The cost multiplier reflects time and compute, not money.

## License

Private — Elcano workspace skill.