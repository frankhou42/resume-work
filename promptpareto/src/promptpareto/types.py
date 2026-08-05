"""Core data types for PromptPareto.

Everything downstream — providers, graders, the optimizer, the report store —
speaks in these dataclasses. Scores are always normalized to [0, 1] so metrics
from different graders are directly comparable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Literal

Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True, slots=True)
class Example:
    """One labeled datapoint. ``target`` is grader-specific (str, dict, number)."""

    id: str
    input: Any
    target: Any
    split: Literal["train", "dev", "test"] = "dev"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PromptCandidate:
    """A prompt under test: an instruction plus optional few-shot exemplars."""

    instruction: str
    few_shot: tuple[Example, ...] = ()
    template: str = "{input}"
    parent_id: str | None = None
    origin: str = "seed"

    @property
    def id(self) -> str:
        """Stable short hash over the fields that change the rendered prompt."""
        shot_ids = ",".join(e.id for e in self.few_shot)
        digest = sha256(f"{self.instruction}|{shot_ids}|{self.template}".encode()).hexdigest()
        return digest[:12]


@dataclass(slots=True)
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass(slots=True)
class Prediction:
    output_text: str
    usage: Usage
    latency_s: float
    cost_usd: float
    provider: str
    model: str
    parsed: Any | None = None


@dataclass(slots=True)
class GradeResult:
    score: float  # normalized to [0, 1]
    passed: bool
    grader: str
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CandidateReport:
    """Aggregate results for one candidate over a set of examples."""

    candidate: PromptCandidate
    n: int
    mean_score: float
    score_ci: tuple[float, float]
    cost_usd_total: float
    latency_p50: float
    scores: list[float] = field(default_factory=list)
    passed: list[bool] = field(default_factory=list)

    @property
    def cost_per_example(self) -> float:
        return self.cost_usd_total / self.n if self.n else 0.0

    def objectives(self) -> dict[str, float]:
        """Objective vector for Pareto sorting (accuracy up, cost/latency down)."""
        return {
            "accuracy": self.mean_score,
            "cost": self.cost_usd_total,
            "latency": self.latency_p50,
        }
