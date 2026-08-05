"""PromptPareto — measured prompt optimization over accuracy, cost, and latency."""

from promptpareto.eval import evaluate, render
from promptpareto.optimize.pareto import ParetoArchive, dominates, pareto_front
from promptpareto.stats import bootstrap_ci, mcnemar, paired_bootstrap_diff
from promptpareto.types import (
    CandidateReport,
    Example,
    GradeResult,
    Prediction,
    PromptCandidate,
    Usage,
)

__version__ = "0.1.0"

__all__ = [
    "CandidateReport",
    "Example",
    "GradeResult",
    "ParetoArchive",
    "Prediction",
    "PromptCandidate",
    "Usage",
    "bootstrap_ci",
    "dominates",
    "evaluate",
    "mcnemar",
    "paired_bootstrap_diff",
    "pareto_front",
    "render",
]
