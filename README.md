# FusionClaw 🐙

**Multi-model deliberation panel. Powered by [NaN Builders](https://nan.builders).**

One model has biases. A panel catches blind spots, surfaces contradictions, and builds consensus through diversity. FusionClaw runs multiple AI models in parallel on the same prompt, then a judge synthesizes their answers into one structured analysis.

**Deliberation panels are token-heavy. Unlimited tokens make them practical.** That's why FusionClaw runs exclusively on [NaN Builders](https://nan.builders) — 500M tokens/month per model, no surprise bills, no rate-limit anxiety.

## Why NaN Builders

| Problem | Typical API | NaN Builders |
|---------|------------|-------------|
| 5-model panel = 5× tokens per prompt | Burns through your quota in hours | 500M tokens/month per model — panels all day |
| Budget anxiety | You hesitate before launching a panel | Launch without budget anxiety |
| Rate limits mid-deliberation | 429 errors break your panel | Generous limits, no throttling |
| Vendor lock-in | Proprietary SDKs | OpenAI-compatible API, drop-in replacement |
| EU data residency | US-hosted, GDPR risk | EU infrastructure |

FusionClaw is the proof. A deliberation panel that spawns 3-5 models per question, each generating 500-2000 tokens, plus a judge that reads all responses. That's 10K-20K tokens per deliberation. Run 100 deliberations a day = 2M tokens/day. That adds up fast on pay-per-token APIs.

**With NaN, token cost stops being the limiting factor.**

## How It Works

```
User prompt → Conductor
                ├── Panel (parallel, different NaN models)
                │   ├── Panelist 1: DeepSeek V4 Flash (reasoning)
                │   ├── Panelist 2: Qwen 3.6 (balanced analysis)
                │   ├── Panelist 3: Gemma 4 (diverse perspective)
                │   └── Panelist 4: Mimo V2.5 (lightweight contrast)
                │
                └── Judge (DeepSeek V4 Flash)
                       → Structured JSON analysis
                → Final synthesized answer
```

1. **Conductor** decides if the task merits deliberation
2. **Panelists** answer the same prompt in parallel, each with a different NaN model
3. **Judge** receives all responses and produces structured analysis: consensus, contradictions, gaps, unique insights, confidence levels
4. **Conductor** synthesizes the final answer from the judge's analysis

## Presets

| Preset | Panel | Judge | Best for |
|--------|-------|-------|----------|
| **quality** | DeepSeek V4 Flash, Qwen 3.6, Gemma 4 | DeepSeek V4 Flash | Architecture, research, complex analysis |
| **fast** | DeepSeek V4 Flash, Qwen 3.6 | DeepSeek V4 Flash | Code review, debugging, quick second opinion |
| **broad** | DeepSeek V4 Flash, Qwen 3.6, Gemma 4, Mimo V2.5 | DeepSeek V4 Flash | Maximum diversity, critical decisions |
| **lean** | DeepSeek V4 Flash, Qwen 3.6 | DeepSeek V4 Flash | Quick sanity check |

## NaN Models Used

| Model | NaN Endpoint | Strength |
|-------|-------------|----------|
| DeepSeek V4 Flash | `nan/deepseek-v4-flash` | Fast reasoning, technical depth |
| Qwen 3.6 | `nan/qwen3.6` | Balanced analysis, versatile |
| Gemma 4 | `nan/gemma4` | Google-quality, diverse perspective |
| Mimo V2.5 | `nan/mimo-v2.5` | Lightweight, contrasting angle |

All models available via [NaN Builders API](https://nan.builders) — OpenAI-compatible, EU-hosted, 500M tokens/month per model.

> **Note:** The model names above (e.g. `deepseek-v4-flash`, `qwen3.6`) are NaN Builders API identifiers. NaN Builders hosts these models on their EU infrastructure with an OpenAI-compatible API. See [nan.builders](https://nan.builders) for the full model list and pricing.

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

## Installation

### Prerequisites

- [NaN Builders](https://nan.builders) account and API key
- [OpenClaw](https://openclaw.ai) installed (FusionClaw is an OpenClaw skill)

### Setup

```bash
# 1. Get your NaN API key at https://nan.builders
# 2. Configure in OpenClaw
openclaw config set providers.nan.apiKey "sk-your-nan-key"

# 3. Install the skill
cp -r fusionclaw ~/.openclaw/workspace/skills/
```

### NaN API Quick Start (without OpenClaw)

```python
import openai

client = openai.OpenAI(
    base_url="https://api.nan.builders/v1",
    api_key="sk-your-nan-key"
)

# Run 3 models in parallel on the same prompt
import concurrent.futures

prompt = "Should we use microservices or a monolith for a team of 5?"

models = ["deepseek-v4-flash", "qwen3.6", "gemma4"]

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = {
        executor.submit(
            client.chat.completions.create,
            model=m,
            messages=[{"role": "user", "content": prompt}]
        ): m for m in models
    }
    results = {f.result().choices[0].message.content: m for f, m in futures.items()}

# Now judge with a final call...
```

That's the whole pattern. FusionClaw just wraps this with structured judging, presets, and safety rails.

## Usage in OpenClaw

Trigger deliberation by:
- Saying "fusion this" or "deliberate on X"
- Asking for a panel analysis
- When your agent detects a task merits deliberation

## When NOT to use FusionClaw

- **Simple questions**: If one model can answer it confidently, don't waste a panel.
- **Time-critical tasks**: Parallel deliberation adds 15-50s of latency.
- **Straightforward edits**: No need for diverse perspectives on a one-line fix.
- **Budget-constrained projects**: If you're on a pay-per-token API, the math changes. FusionClaw assumes NaN's flat-rate model.

## Why Not OpenRouter / Other Providers?

You can absolutely run a deliberation panel on any provider. But:

- **OpenRouter**: Pay per token. A 5-model panel with judge = 6 API calls × 1000 tokens average = 6K tokens per question. At GPT-4 prices, that's ~$0.18/question. 100 questions/day = $18/day = $540/month. With NaN: €70/month flat.
- **Direct APIs**: Same math, more integration work.
- **Local models**: Free but you need GPUs, and model diversity is limited by VRAM.

NaN Builders hits the sweet spot: enough models for genuine diversity, unlimited tokens for real-world usage, EU-hosted for compliance, OpenAI-compatible for easy integration.

## Cost Comparison

| Setup | Monthly cost | Deliberations/day possible |
|-------|------------|--------------------------|
| OpenRouter (frontier models) | $500+ | ~100 |
| OpenAI direct (GPT-4 class) | $400+ | ~80 |
| NaN Builders (4 models) | €70 | Unlimited* |
| Local (4 models, 2× A100) | $800+ (hardware) | Unlimited |

*Within 500M tokens/month per model fair use. That's roughly 250K deliberations/month under fair use.

## License

MIT — Use it, fork it, sell it. Just point back to NaN Builders.

## Links

- [NaN Builders](https://nan.builders) — Get your API key
- [OpenClaw](https://openclaw.ai) — Agent framework that runs FusionClaw
- [OpenRouter Fusion](https://openrouter.ai/docs/guides/routing/routers/fusion-router) — The original inspiration