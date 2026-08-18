# FusionClaw Presets Reference

All presets use [NaN Builders](https://nan.builders) models exclusively.

## Quality (default)

Best for architecture, research, complex analysis.

| Role | Model | NaN Endpoint |
|------|-------|-------------|
| Panelist 1 | DeepSeek V4 Flash | `nan/deepseek-v4-flash` |
| Panelist 2 | Qwen 3.6 | `nan/qwen3.6` |
| Panelist 3 | Gemma 4 | `nan/gemma4` |
| Judge | DeepSeek V4 Flash | `nan/deepseek-v4-flash` |

Tokens per deliberation: ~15-25K. Time: ~15-40s.

## Fast

Best for code review, debugging, quick second opinions.

| Role | Model | NaN Endpoint |
|------|-------|-------------|
| Panelist 1 | DeepSeek V4 Flash | `nan/deepseek-v4-flash` |
| Panelist 2 | Qwen 3.6 | `nan/qwen3.6` |
| Judge | DeepSeek V4 Flash | `nan/deepseek-v4-flash` |

Tokens per deliberation: ~8-15K. Time: ~8-20s.

## Broad

Maximum diversity for critical decisions.

| Role | Model | NaN Endpoint |
|------|-------|-------------|
| Panelist 1 | DeepSeek V4 Flash | `nan/deepseek-v4-flash` |
| Panelist 2 | Qwen 3.6 | `nan/qwen3.6` |
| Panelist 3 | Gemma 4 | `nan/gemma4` |
| Panelist 4 | Mimo V2.5 | `nan/mimo-v2.5` |
| Judge | DeepSeek V4 Flash | `nan/deepseek-v4-flash` |

Tokens per deliberation: ~20-35K. Time: ~20-50s.

## Lean

Quick deliberation with 2 panelists.

| Role | Model | NaN Endpoint |
|------|-------|-------------|
| Panelist 1 | DeepSeek V4 Flash | `nan/deepseek-v4-flash` |
| Panelist 2 | Qwen 3.6 | `nan/qwen3.6` |
| Judge | DeepSeek V4 Flash | `nan/deepseek-v4-flash` |

Tokens per deliberation: ~8-12K. Time: ~10-25s.

## Custom

Override any preset by specifying models explicitly. Minimum 2 panelists, maximum 8.

Available NaN models for custom panels:

| Model | Endpoint | Profile |
|-------|----------|---------|
| DeepSeek V4 Flash | `nan/deepseek-v4-flash` | Fast reasoning, technical |
| Qwen 3.6 | `nan/qwen3.6` | Balanced, versatile |
| Gemma 4 | `nan/gemma4` | Google-quality, diverse |
| Mimo V2.5 | `nan/mimo-v2.5` | Lightweight, contrasting |

## Preset Selection Heuristics

| Task type | Recommended preset |
|-----------|-------------------|
| Architecture decisions | quality |
| Code review | fast |
| Security analysis | broad |
| Research questions | quality |
| Bug debugging | fast |
| Strategic decisions | broad |
| Quick second opinion | lean |

## Token Economics

With NaN Builders' 500M tokens/month per model, here's how many deliberations you can run:

| Preset | Tokens/deliberation | Deliberations/month (per model) |
|--------|-------------------|-------------------------------|
| lean | ~10K | ~50,000 |
| fast | ~12K | ~41,000 |
| quality | ~20K | ~25,000 |
| broad | ~28K | ~17,000 |

You will not hit these limits. Run panels without counting.