# FusionClaw Presets Reference

## Quality (default)

Best for architecture, research, complex analysis.

| Role | Model | Alias |
|------|-------|-------|
| Panelist 1 | ollama/glm-5.1:cloud | glm5 |
| Panelist 2 | ollama/kimi-k2.6:cloud | kimi |
| Panelist 3 | ollama/deepseek-v4-pro:cloud | deepseek |
| Judge | ollama/glm-5.1:cloud | glm5 |

Cost: ~4× single model. Time: ~45-90s.

## Fast

Best for code review, debugging, quick second opinions.

| Role | Model | Alias |
|------|-------|-------|
| Panelist 1 | ollama/kimi-k2.7-code:cloud | kimi27code |
| Panelist 2 | ollama/qwen3-coder-next:cloud | qwencoder |
| Judge | ollama/kimi-k2.7-code:cloud | kimi27code |

Cost: ~3×. Time: ~20-40s.

## Broad

Maximum diversity for critical decisions.

| Role | Model | Alias |
|------|-------|-------|
| Panelist 1 | ollama/glm-5.1:cloud | glm5 |
| Panelist 2 | ollama/kimi-k2.6:cloud | kimi |
| Panelist 3 | ollama/deepseek-v4-pro:cloud | deepseek |
| Panelist 4 | ollama/nemotron-3-super:cloud | nemotron |
| Judge | ollama/glm-5.1:cloud | glm5 |

Cost: ~5×. Time: ~60-120s.

## Lean

Quick deliberation with 2 panelists.

| Role | Model | Alias |
|------|-------|-------|
| Panelist 1 | ollama/glm-5.1:cloud | glm5 |
| Panelist 2 | ollama/kimi-k2.6:cloud | kimi |
| Judge | ollama/glm-5.1:cloud | glm5 |

Cost: ~3×. Time: ~30-60s.

## Hybrid (with OpenRouter Fusion)

For web-augmented deliberation. Uses one local panelist + OpenRouter Fusion as second panelist.

| Role | Model | Alias |
|------|-------|-------|
| Panelist 1 | ollama/glm-5.1:cloud | glm5 |
| Panelist 2 | openrouter/openrouter/fusion | fusion |
| Judge | ollama/glm-5.1:cloud | glm5 |

Cost: ~3× + OpenRouter costs. Time: ~60-120s.

## Custom

Override any preset by specifying models explicitly. Minimum 2 panelists, maximum 8.

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
| Web-dependent research | hybrid |