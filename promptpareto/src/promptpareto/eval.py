"""Evaluation engine: render a candidate over examples, grade, aggregate.

Kept synchronous and dependency-light for v0.1 — the provider layer is where
concurrency would be added later. The output is a :class:`CandidateReport` with
a bootstrapped confidence interval on the mean score.
"""

from __future__ import annotations

import statistics

from promptpareto.graders import Grader
from promptpareto.providers import Provider, ProviderRequest
from promptpareto.stats import bootstrap_ci
from promptpareto.types import CandidateReport, Example, PromptCandidate


def render(candidate: PromptCandidate, ex: Example) -> list[dict[str, str]]:
    """Build provider messages: system instruction, few-shot turns, then input."""
    messages: list[dict[str, str]] = [{"role": "system", "content": candidate.instruction}]
    for shot in candidate.few_shot:
        messages.append({"role": "user", "content": str(shot.input)})
        messages.append({"role": "assistant", "content": str(shot.target)})
    body = candidate.template.replace("{input}", str(ex.input))
    messages.append({"role": "user", "content": body})
    return messages


def evaluate(
    candidate: PromptCandidate,
    examples: list[Example],
    provider: Provider,
    model: str,
    grader: Grader,
    *,
    seed: int = 0,
) -> CandidateReport:
    scores: list[float] = []
    passed: list[bool] = []
    latencies: list[float] = []
    cost_total = 0.0

    for ex in examples:
        req = ProviderRequest(messages=render(candidate, ex), model=model, seed=seed)
        pred = provider.complete(req)
        result = grader.grade(pred, ex)
        scores.append(result.score)
        passed.append(result.passed)
        latencies.append(pred.latency_s)
        cost_total += pred.cost_usd

    mean = statistics.fmean(scores) if scores else 0.0
    ci = bootstrap_ci(scores, seed=seed)
    p50 = statistics.median(latencies) if latencies else 0.0
    return CandidateReport(
        candidate=candidate,
        n=len(examples),
        mean_score=mean,
        score_ci=ci,
        cost_usd_total=cost_total,
        latency_p50=p50,
        scores=scores,
        passed=passed,
    )
