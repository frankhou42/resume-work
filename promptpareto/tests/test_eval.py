"""End-to-end eval + optimizer-comparison test, fully offline via MockProvider."""

from promptpareto.eval import evaluate, render
from promptpareto.graders import ExactMatch
from promptpareto.providers import MockProvider
from promptpareto.stats import paired_bootstrap_diff
from promptpareto.types import Example, PromptCandidate

EXAMPLES = [
    Example(id="1", input="capital of France", target="Paris"),
    Example(id="2", input="capital of Japan", target="Tokyo"),
    Example(id="3", input="capital of Italy", target="Rome"),
    Example(id="4", input="capital of Spain", target="Madrid"),
]


def test_render_includes_instruction_and_fewshot():
    shot = Example(id="s", input="capital of Peru", target="Lima")
    cand = PromptCandidate(instruction="Answer with the city only.", few_shot=(shot,))
    msgs = render(cand, EXAMPLES[0])
    assert msgs[0] == {"role": "system", "content": "Answer with the city only."}
    assert any(m["content"] == "Lima" for m in msgs)  # few-shot answer present
    assert msgs[-1]["content"].endswith("capital of France")


def test_good_prompt_beats_bad_prompt_endtoend():
    # A "good" provider knows every capital; a "bad" one always says "I don't know".
    good = MockProvider(
        responses={
            "France": "Paris",
            "Japan": "Tokyo",
            "Italy": "Rome",
            "Spain": "Madrid",
        },
        default="I don't know",
    )
    bad = MockProvider(default="I don't know")
    cand = PromptCandidate(instruction="Answer with the city.")
    grader = ExactMatch()

    good_rep = evaluate(cand, EXAMPLES, good, "gpt-4o-mini", grader)
    bad_rep = evaluate(cand, EXAMPLES, bad, "gpt-4o-mini", grader)

    assert good_rep.mean_score == 1.0
    assert bad_rep.mean_score == 0.0
    # paired comparison should call the win significant
    diff = paired_bootstrap_diff(good_rep.scores, bad_rep.scores, seed=1)
    assert diff.delta == 1.0 and diff.significant


def test_report_objectives_shape():
    p = MockProvider(default="Paris")
    rep = evaluate(PromptCandidate(instruction="x"), EXAMPLES, p, "gpt-4o-mini", ExactMatch())
    obj = rep.objectives()
    assert set(obj) == {"accuracy", "cost", "latency"}
    assert rep.cost_per_example >= 0.0
