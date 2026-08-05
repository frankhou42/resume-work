from promptpareto.graders import ExactMatch, JsonFieldMatch, TokenF1, get_grader
from promptpareto.types import Example, Prediction, Usage


def _pred(text: str, parsed=None) -> Prediction:
    return Prediction(
        output_text=text,
        usage=Usage(),
        latency_s=0.0,
        cost_usd=0.0,
        provider="mock",
        model="m",
        parsed=parsed,
    )


def _ex(target) -> Example:
    return Example(id="1", input="q", target=target)


def test_exact_match_normalizes():
    g = ExactMatch()
    assert g.grade(_pred("The Answer."), _ex("answer")).passed
    assert not g.grade(_pred("wrong"), _ex("answer")).passed


def test_token_f1_partial_overlap():
    g = TokenF1()
    r = g.grade(_pred("quick brown fox"), _ex("the quick red fox"))
    assert 0.0 < r.score < 1.0  # partial overlap


def test_token_f1_perfect():
    g = TokenF1()
    assert g.grade(_pred("hello world"), _ex("hello world")).score == 1.0


def test_json_field_match_partial():
    g = JsonFieldMatch()
    r = g.grade(
        _pred('{"name": "Frank", "city": "Austin"}'), _ex({"name": "Frank", "city": "Dallas"})
    )
    assert r.score == 0.5
    assert not r.passed


def test_json_field_match_unparseable():
    g = JsonFieldMatch()
    r = g.grade(_pred("not json"), _ex({"a": "b"}))
    assert r.score == 0.0
    assert r.detail["error"] == "unparseable"


def test_json_field_match_uses_parsed():
    g = JsonFieldMatch()
    r = g.grade(_pred("ignored", parsed={"a": "b"}), _ex({"a": "b"}))
    assert r.score == 1.0


def test_registry():
    assert isinstance(get_grader("exact_match"), ExactMatch)
    try:
        get_grader("nope")
        raise AssertionError("expected KeyError")
    except KeyError:
        pass
