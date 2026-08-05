# PromptPareto

[![CI](https://github.com/frankhou42/promptpareto/actions/workflows/checks.yml/badge.svg)](https://github.com/frankhou42/promptpareto/actions/workflows/checks.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**Turn prompt engineering into a measured optimization problem.**

PromptPareto evaluates prompt candidates across multiple model providers
(OpenAI, Anthropic, local Ollama), then searches for better prompts while
maintaining a **Pareto front over accuracy, cost, and latency**. Every claimed
improvement is backed by a **held-out test set and a bootstrap confidence
interval** — not a single lucky run.

> Why this exists: "prompt engineering" is usually vibes. PromptPareto makes it
> an experiment — with graders, statistical tests, and an explicit accuracy /
> cost / latency tradeoff — and guards against the optimizer *gaming* an LLM
> judge (a scaled-down reward-hacking problem).

## Install

```bash
pip install promptpareto            # core
pip install "promptpareto[all]"     # + OpenAI, Anthropic, Ollama providers
```

## Quickstart

```python
from promptpareto import evaluate, paired_bootstrap_diff, PromptCandidate, Example
from promptpareto.graders import ExactMatch
from promptpareto.providers import get_provider

provider, model = get_provider("ollama:llama3.2")   # local + free
examples = [
    Example(id="1", input="capital of France", target="Paris"),
    Example(id="2", input="capital of Japan",  target="Tokyo"),
]

baseline = PromptCandidate(instruction="Answer the question.")
improved = PromptCandidate(instruction="Answer with ONLY the city name, nothing else.")

b = evaluate(baseline, examples, provider, model, ExactMatch())
i = evaluate(improved, examples, provider, model, ExactMatch())

diff = paired_bootstrap_diff(i.scores, b.scores)
print(f"improvement: {diff.delta:+.3f}  95% CI {diff.ci}  significant={diff.significant}")
```

## What's inside

| Module | Responsibility |
|--------|----------------|
| `providers/` | Thin per-provider adapters (OpenAI, Anthropic, Ollama, Mock). Normalizes tokens, latency, and USD cost. |
| `graders/` | Rule-based graders (exact match, token-F1, JSON-field) — the un-gameable honesty anchor. |
| `eval.py` | Render a candidate over examples → grade → aggregate with a bootstrap CI. |
| `stats.py` | Bootstrap CIs, **paired** bootstrap diff, McNemar's exact test, power/`n` sizing. |
| `optimize/pareto.py` | Domination test + non-dominated front + archive. |

## Design notes

- **Paired comparisons.** The same examples run through both prompts, so the
  bootstrap is over per-example *differences* — much tighter than comparing two
  independent samples.
- **Anthropic quirk handled.** Current Claude models reject `temperature` /
  `budget_tokens` (HTTP 400); the Anthropic adapter drops them, with a test that
  fails if that ever regresses.
- **Local-first.** Ollama runs at `$0`, so you can iterate and demo entirely
  offline; provider cost only accrues for hosted models.

## Roadmap

- v0.1 (this release): multi-provider eval, rule graders, paired stats, Pareto archive.
- Next: the evolutionary optimizer (instruction rewriting + few-shot selection),
  LLM-as-judge with anti-gaming checks, a React/TS leaderboard, and PyPI publish.

## License

[MIT](LICENSE) © Frank Hou
