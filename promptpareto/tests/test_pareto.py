from promptpareto.optimize.pareto import ParetoArchive, dominates, pareto_front
from promptpareto.types import CandidateReport, PromptCandidate


def _report(acc: float, cost: float, lat: float) -> CandidateReport:
    return CandidateReport(
        candidate=PromptCandidate(instruction=f"acc{acc}-c{cost}-l{lat}"),
        n=10,
        mean_score=acc,
        score_ci=(acc, acc),
        cost_usd_total=cost,
        latency_p50=lat,
    )


def test_dominates_basic():
    better = {"accuracy": 0.9, "cost": 1.0, "latency": 1.0}
    worse = {"accuracy": 0.8, "cost": 2.0, "latency": 2.0}
    assert dominates(better, worse)
    assert not dominates(worse, better)


def test_dominates_requires_strict_improvement():
    same = {"accuracy": 0.9, "cost": 1.0, "latency": 1.0}
    assert not dominates(same, dict(same))  # identical -> no domination


def test_pareto_front_keeps_tradeoffs():
    # high acc/high cost vs low acc/low cost -> both on the front
    a = _report(0.9, 10.0, 5.0)
    b = _report(0.7, 1.0, 1.0)
    dominated = _report(0.6, 20.0, 9.0)
    front = pareto_front([a, b, dominated])
    assert a in front and b in front
    assert dominated not in front


def test_archive_tracks_front_and_best():
    arc = ParetoArchive()
    arc.add(_report(0.7, 1.0, 1.0))
    entered = arc.add(_report(0.9, 2.0, 2.0))  # not dominated -> enters front
    assert entered
    best = arc.best("accuracy")
    assert best is not None and best.mean_score == 0.9
    cheapest = arc.best("cost")
    assert cheapest is not None and cheapest.cost_usd_total == 1.0
