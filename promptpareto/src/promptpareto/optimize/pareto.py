"""Pareto-front bookkeeping.

Objectives are normalized to "higher is better" before comparison: accuracy is
kept as-is, cost and latency are negated. A candidate *dominates* another if it
is at least as good on every objective and strictly better on one.
"""

from __future__ import annotations

from promptpareto.types import CandidateReport

# direction per objective: +1 = maximize, -1 = minimize
DIRECTIONS = {"accuracy": 1.0, "cost": -1.0, "latency": -1.0}


def _normalized(obj: dict[str, float]) -> dict[str, float]:
    return {k: DIRECTIONS[k] * v for k, v in obj.items() if k in DIRECTIONS}


def dominates(a: dict[str, float], b: dict[str, float]) -> bool:
    """True if objective vector ``a`` Pareto-dominates ``b``."""
    na, nb = _normalized(a), _normalized(b)
    keys = na.keys()
    at_least_as_good = all(na[k] >= nb[k] for k in keys)
    strictly_better = any(na[k] > nb[k] for k in keys)
    return at_least_as_good and strictly_better


def pareto_front(reports: list[CandidateReport]) -> list[CandidateReport]:
    """Return the non-dominated subset of ``reports``."""
    front: list[CandidateReport] = []
    for r in reports:
        ro = r.objectives()
        if any(dominates(other.objectives(), ro) for other in reports if other is not r):
            continue
        front.append(r)
    return front


class ParetoArchive:
    """Accumulates candidate reports and tracks the current non-dominated front."""

    def __init__(self) -> None:
        self._reports: list[CandidateReport] = []

    def add(self, report: CandidateReport) -> bool:
        """Add a report; return True if it entered the (new) Pareto front."""
        self._reports.append(report)
        return report in pareto_front(self._reports)

    def front(self) -> list[CandidateReport]:
        return pareto_front(self._reports)

    def all(self) -> list[CandidateReport]:
        return list(self._reports)

    def best(self, objective: str = "accuracy") -> CandidateReport | None:
        if not self._reports:
            return None
        maximize = DIRECTIONS.get(objective, 1.0) > 0
        return (max if maximize else min)(self._reports, key=lambda r: r.objectives()[objective])
