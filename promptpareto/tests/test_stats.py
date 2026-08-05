import numpy as np

from promptpareto.stats import (
    bootstrap_ci,
    mcnemar,
    paired_bootstrap_diff,
    required_n,
)


def test_bootstrap_ci_brackets_mean():
    scores = [0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0]
    lo, hi = bootstrap_ci(scores, seed=1)
    assert lo <= np.mean(scores) <= hi
    assert 0.0 <= lo <= hi <= 1.0


def test_bootstrap_ci_empty():
    assert bootstrap_ci([]) == (0.0, 0.0)


def test_paired_bootstrap_detects_clear_win():
    a = [1.0] * 40  # always right
    b = [0.0] * 40  # always wrong
    res = paired_bootstrap_diff(a, b, seed=1)
    assert res.delta == 1.0
    assert res.significant
    assert res.ci[0] > 0


def test_paired_bootstrap_no_diff_not_significant():
    vals = [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0]
    res = paired_bootstrap_diff(vals, vals, seed=1)
    assert res.delta == 0.0
    assert not res.significant


def test_paired_requires_equal_length():
    try:
        paired_bootstrap_diff([1.0], [1.0, 0.0])
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_mcnemar_symmetric_is_one():
    # equal discordant pairs -> no evidence of difference
    a = [True, False, True, False]
    b = [False, True, False, True]
    assert mcnemar(a, b) == 1.0


def test_mcnemar_all_discordant_one_direction():
    a = [True] * 10
    b = [False] * 10
    assert mcnemar(a, b) < 0.01  # strong evidence a > b


def test_required_n_shrinks_with_larger_effect():
    assert required_n(effect=0.02) > required_n(effect=0.10)
