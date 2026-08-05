"""Graders: turn a model prediction + gold target into a normalized [0,1] score.

Rule-based graders (exact match, token-F1, JSON-field) are cheap and
un-gameable — they are the honesty anchor that an LLM judge is checked against.
"""

from __future__ import annotations

import re
import string
from collections import Counter
from typing import Protocol

from promptpareto.types import Example, GradeResult, Prediction


class Grader(Protocol):
    name: str

    def grade(self, pred: Prediction, ex: Example) -> GradeResult: ...


def _normalize(text: str) -> str:
    """SQuAD-style normalization: lowercase, strip punctuation/articles/space."""
    text = text.lower()
    text = "".join(ch for ch in text if ch not in string.punctuation)
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    return " ".join(text.split())


class ExactMatch:
    name = "exact_match"

    def grade(self, pred: Prediction, ex: Example) -> GradeResult:
        hit = _normalize(pred.output_text) == _normalize(str(ex.target))
        return GradeResult(score=1.0 if hit else 0.0, passed=hit, grader=self.name)


class TokenF1:
    name = "token_f1"

    def grade(self, pred: Prediction, ex: Example) -> GradeResult:
        pred_tokens = _normalize(pred.output_text).split()
        gold_tokens = _normalize(str(ex.target)).split()
        if not pred_tokens or not gold_tokens:
            f1 = 1.0 if pred_tokens == gold_tokens else 0.0
            return GradeResult(score=f1, passed=f1 == 1.0, grader=self.name)
        common = Counter(pred_tokens) & Counter(gold_tokens)
        overlap = sum(common.values())
        if overlap == 0:
            return GradeResult(score=0.0, passed=False, grader=self.name)
        precision = overlap / len(pred_tokens)
        recall = overlap / len(gold_tokens)
        f1 = 2 * precision * recall / (precision + recall)
        return GradeResult(
            score=f1,
            passed=f1 >= 0.99,
            grader=self.name,
            detail={"precision": precision, "recall": recall},
        )


class JsonFieldMatch:
    """Parse the model output as JSON and score per-field exact match.

    ``ex.target`` must be a dict; score is the fraction of target fields that
    match (case-insensitive string compare).
    """

    name = "json_field_match"

    def grade(self, pred: Prediction, ex: Example) -> GradeResult:
        import json

        if not isinstance(ex.target, dict):
            raise ValueError("JsonFieldMatch requires a dict target")
        try:
            obj = pred.parsed if pred.parsed is not None else json.loads(pred.output_text)
        except (json.JSONDecodeError, TypeError):
            return GradeResult(
                score=0.0, passed=False, grader=self.name, detail={"error": "unparseable"}
            )
        if not isinstance(obj, dict):
            return GradeResult(score=0.0, passed=False, grader=self.name)
        hits = sum(
            1
            for k, v in ex.target.items()
            if str(obj.get(k, "")).strip().lower() == str(v).strip().lower()
        )
        score = hits / len(ex.target) if ex.target else 0.0
        return GradeResult(
            score=score,
            passed=score == 1.0,
            grader=self.name,
            detail={"matched": hits, "total": len(ex.target)},
        )


BUILTINS: dict[str, type] = {
    ExactMatch.name: ExactMatch,
    TokenF1.name: TokenF1,
    JsonFieldMatch.name: JsonFieldMatch,
}


def get_grader(name: str) -> Grader:
    if name not in BUILTINS:
        raise KeyError(f"unknown grader '{name}'; available: {list(BUILTINS)}")
    return BUILTINS[name]()  # type: ignore[return-value]
