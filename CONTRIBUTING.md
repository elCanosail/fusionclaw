# Contributing to FusionClaw

FusionClaw is a small, focused project. We welcome contributions that improve the core deliberation pattern or expand NaN Builders model support.

## Quick Start

```bash
git clone https://github.com/elCanosail/fusionclaw.git
cd fusionclaw
pip install openai  # only dependency for example.py
```

## Areas We Need Help With

- **New presets**: Domain-specific panel compositions (legal, medical, financial)
- **Judge improvements**: Better structured analysis prompts
- **Model benchmarks**: Comparing NaN model combinations for different task types
- **Integration examples**: How you use FusionClaw in your workflow

## Guidelines

1. Keep it simple. FusionClaw's value is its simplicity.
2. No provider lock-in. NaN Builders only — this is a showcase, not a general-purpose tool.
3. Test example.py compiles: `python3 -c "compile(open('example.py').read(), 'example.py', 'exec')"`
4. Markdown files use the existing style (tables, concise prose).
5. PRs should be small and focused.

## Reporting Issues

Use GitHub Issues. Include:
- What you expected
- What happened
- Your NaN preset and models used
- The question/prompt (if not sensitive)

## License

By contributing, you agree your contributions are licensed under the MIT License.