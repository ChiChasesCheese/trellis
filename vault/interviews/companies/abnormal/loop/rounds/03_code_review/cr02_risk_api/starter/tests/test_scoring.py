from riskapi.scoring import compute_risk, level_for


def test_score_is_capped_sum():
    r = compute_risk([("a", 70, "t"), ("b", 60, "t")])
    assert r.score == 100 and r.level == "high"


def test_factors_are_top_five_by_weight():
    r = compute_risk([(f"k{i}", i, "t") for i in range(1, 9)])
    assert [f["weight"] for f in r.factors] == [8, 7, 6, 5, 4]


def test_levels():
    assert [level_for(s) for s in (0, 29, 30, 69, 70)] == ["low", "low", "medium", "medium", "high"]
