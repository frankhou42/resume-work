"""Statistical rigor for prompt comparisons.

The whole point of PromptPareto is that a claimed win is backed by a
confidence interval, not a single lucky run. Comparisons are *paired* (the same
examples run through both prompts), which gives much tighter intervals than
comparing two independent samples.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def bootstrap_ci(
    scores: list[float],
    *,
    n_boot: int = 10_000,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float, float]:
    """Percentile bootstrap CI for the mean of ``scores``."""
    if not scores:
        return (0.0, 0.0)
    rng = np.random.default_rng(seed)
    arr = np.asarray(scores, dtype=float)
    means = arr[rng.integers(0, len(arr), size=(n_boot, len(arr)))].mean(axis=1)
    lo = float(np.quantile(means, alpha / 2))
    hi = float(np.quantile(means, 1 - alpha / 2))
    return (lo, hi)


@dataclass(slots=True)
class DiffResult:
    delta: float  # mean(a) - mean(b)
    ci: tuple[float, float]
    significant: bool  # CI excludes 0


def paired_bootstrap_diff(
    a: list[float],
    b: list[float],
    *,
    n_boot: int = 10_000,
    alpha: float = 0.05,
    seed: int = 0,
) -> DiffResult:
    """Paired bootstrap on the per-example difference a[i] - b[i].

    ``a`` and ``b`` must be aligned: same example at each index.
    """
    if len(a) != len(b):
        raise ValueError("paired_bootstrap_diff requires equal-length aligned scores")
    if not a:
        return DiffResult(0.0, (0.0, 0.0), False)
    rng = np.random.default_rng(seed)
    diffs = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    boot = diffs[rng.integers(0, len(diffs), size=(n_boot, len(diffs)))].mean(axis=1)
    lo = float(np.quantile(boot, alpha / 2))
    hi = float(np.quantile(boot, 1 - alpha / 2))
    delta = float(diffs.mean())
    return DiffResult(delta=delta, ci=(lo, hi), significant=(lo > 0 or hi < 0))


def mcnemar(a_correct: list[bool], b_correct: list[bool]) -> float:
    """McNemar's test for paired binary outcomes. Returns a two-sided p-value.

    Uses the exact binomial test on discordant pairs, which is valid for small n
    (where the chi-square approximation is unreliable).
    """
    if len(a_correct) != len(b_correct):
        raise ValueError("mcnemar requires equal-length aligned outcomes")
    # b = a right, b wrong; c = a wrong, b right
    b = sum(1 for x, y in zip(a_correct, b_correct, strict=True) if x and not y)
    c = sum(1 for x, y in zip(a_correct, b_correct, strict=True) if not x and y)
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    # two-sided exact binomial p at p=0.5
    from math import comb

    tail = sum(comb(n, i) for i in range(k + 1)) / (2**n)
    return min(1.0, 2 * tail)


def required_n(effect: float = 0.05, alpha: float = 0.05, power: float = 0.8) -> int:
    """Approximate paired-sample size to detect a mean score difference ``effect``.

    Uses a normal approximation with a conservative unit-variance assumption
    (scores in [0,1]); reported to the user as a floor, not a guarantee.
    """
    # z-values without scipy: standard approximations
    z_alpha = 1.959963984540054 if alpha == 0.05 else _z(1 - alpha / 2)
    z_beta = 0.8416212335729143 if power == 0.8 else _z(power)
    sd = 0.5  # max std for a [0,1] variable
    n = ((z_alpha + z_beta) * sd / effect) ** 2
    return max(1, int(np.ceil(n)))


def _z(p: float) -> float:
    """Inverse standard-normal CDF (Acklam's approximation) — avoids scipy dep."""
    a = [
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    ]
    b = [
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464968e00,
        2.938163982698783e00,
    ]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00, 3.754408661907416e00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = np.sqrt(-2 * np.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
        )
    if p <= phigh:
        q = p - 0.5
        r = q * q
        return (
            (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5])
            * q
            / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
        )
    q = np.sqrt(-2 * np.log(1 - p))
    return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
        (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
    )
