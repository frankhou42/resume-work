"""Offline end-to-end demo — no API keys, no network.

Runs two prompt candidates through a mock provider over a small labeled set,
grades with exact match, and reports a paired-bootstrap comparison with a 95%
confidence interval. Run:  python examples/demo.py
"""

from promptpareto import PromptCandidate, evaluate, paired_bootstrap_diff
from promptpareto.graders import ExactMatch
from promptpareto.optimize.pareto import ParetoArchive
from promptpareto.providers import MockProvider
from promptpareto.types import Example

# A tiny "capitals" task.
EXAMPLES = [
    Example(id="fr", input="capital of France", target="Paris"),
    Example(id="jp", input="capital of Japan", target="Tokyo"),
    Example(id="it", input="capital of Italy", target="Rome"),
    Example(id="es", input="capital of Spain", target="Madrid"),
    Example(id="de", input="capital of Germany", target="Berlin"),
    Example(id="ca", input="capital of Canada", target="Ottawa"),
]

# Mock model that answers correctly only when the instruction nudges it to be
# terse (simulating a real prompt-sensitivity effect the optimizer would find).
KNOWLEDGE = {
    "France": "Paris", "Japan": "Tokyo", "Italy": "Rome",
    "Spain": "Madrid", "Germany": "Berlin", "Canada": "Ottawa",
}


def make_provider(good: bool) -> MockProvider:
    # "good" prompt -> terse correct answers; "bad" -> a chatty wrong prefix.
    if good:
        return MockProvider(responses=KNOWLEDGE, default="unknown")
    return MockProvider(default="I think it might be ...")


def main() -> None:
    grader = ExactMatch()
    baseline = PromptCandidate(instruction="Tell me about the capital.")
    improved = PromptCandidate(instruction="Answer with ONLY the city name.")

    base_rep = evaluate(baseline, EXAMPLES, make_provider(good=False), "gpt-4o-mini", grader)
    imp_rep = evaluate(improved, EXAMPLES, make_provider(good=True), "gpt-4o-mini", grader)

    archive = ParetoArchive()
    archive.add(base_rep)
    archive.add(imp_rep)

    diff = paired_bootstrap_diff(imp_rep.scores, base_rep.scores, seed=0)

    print("PromptPareto demo — capitals task\n" + "=" * 40)
    print(f"baseline  accuracy={base_rep.mean_score:.2f}  95% CI {fmt(base_rep.score_ci)}")
    print(f"improved  accuracy={imp_rep.mean_score:.2f}  95% CI {fmt(imp_rep.score_ci)}")
    print("-" * 40)
    print(f"improvement: {diff.delta:+.3f}   95% CI {fmt(diff.ci)}")
    print(f"significant (CI excludes 0): {diff.significant}")
    print("-" * 40)
    print("Pareto front:")
    for r in archive.front():
        o = r.objectives()
        print(f"  {r.candidate.id}  acc={o['accuracy']:.2f}  cost=${o['cost']:.4f}")


def fmt(ci: tuple[float, float]) -> str:
    return f"[{ci[0]:.2f}, {ci[1]:.2f}]"


if __name__ == "__main__":
    main()
