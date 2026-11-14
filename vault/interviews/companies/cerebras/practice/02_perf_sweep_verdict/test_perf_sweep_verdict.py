from __future__ import annotations

from pathlib import Path

import pytest

DATA = Path(__file__).resolve().parent / "data"
FILES = [DATA / "sweep_ab.csv", DATA / "Model_C_profile_2.csv"]


def pt(impl, c, ttft, tps_user, total=None, tpot=None, model="X", profile="1"):
    total = tps_user * c if total is None else total
    tpot = 1000 / tps_user if tpot is None else tpot
    return impl.Point(model, profile, 1000, 200, c, ttft, tpot, tps_user, total)


# ---------------------------------------------------------------- Part 1: header contract


@pytest.mark.part1
@pytest.mark.parametrize("raw,norm", [("TTFT (ms)", "ttftms"), ("tok/s/user", "tokpersperuser"),
                                      ("Total tok/s", "totaltokpers"), ("batch_size", "batchsize"),
                                      ("  ISL ", "isl")])
def test_normalize_header(impl, raw, norm):
    assert impl.normalize_header(raw) == norm


@pytest.mark.part1
def test_map_headers_two_styles(impl):
    a = impl.map_headers(["model", "profile", "input_tokens", "output_tokens", "concurrency", "TTFT (ms)",
                          "TPOT (ms)", "tok/s/user", "total tok/s"])
    assert a["ttft_ms"] == ("TTFT (ms)", 1) and a["tps_total"] == ("total tok/s", 1)
    b = impl.map_headers(["ISL", "OSL", "batch_size", "ttft_s", "ITL (ms)", "Tokens/s per user", "Throughput",
                          "notes"])
    assert b["ttft_ms"] == ("ttft_s", 1000), "seconds must be converted to milliseconds"
    assert b["concurrency"] == ("batch_size", 1) and b["tpot_ms"] == ("ITL (ms)", 1)
    assert "model" not in b and "profile" not in b


@pytest.mark.part1
def test_parse_both_files(impl):
    pts, an = impl.load_all(FILES)
    assert len(pts) == 24 + 4 - 1  # one row has an empty cell
    c = [p for p in pts if p.model == "C"]
    assert {p.profile for p in c} == {"2"} and len(c) == 4
    c16 = next(p for p in c if p.concurrency == 16)
    assert c16.ttft_ms == pytest.approx(3006.7) and c16.tps_total == pytest.approx(4480.0)
    assert [(a.model, a.profile, a.concurrency, a.kind) for a in an] == [("B", "1", 4, "missing_value")]


@pytest.mark.part1
def test_new_model_needs_no_code(impl, tmp_path):
    p = tmp_path / "Model_L_profile_7.csv"
    p.write_text("Input Length,Output Length,Concurrent Users,Time to First Token (s),Inter-token Latency (ms),"
                 "Tokens per Second per User,System Throughput\n"
                 "2000,500,8,0.25,2.0,500,4000\n2000,500,32,0.40,2.5,400,12800\n")
    pts, an = impl.parse_sweep(p)
    assert an == [] and [(x.model, x.profile, x.concurrency) for x in pts] == [("L", "7", 8), ("L", "7", 32)]
    assert pts[0].ttft_ms == pytest.approx(250.0)
    v = impl.verdicts(pts, impl.SLA(16, 1000, 300))
    assert [(x.model, x.profile, x.color, x.concurrency_used) for x in v] == [("L", "7", "green", 32)]


# ---------------------------------------------------------------- Part 2: verdicts


@pytest.mark.part2
def test_verdicts_on_data(impl):
    pts, an = impl.load_all(FILES)
    an = an + impl.find_anomalies(pts)
    got = {(v.model, v.profile): v.color for v in impl.verdicts(pts, impl.SLA(16, 1400, 300), an)}
    assert got == {("A", "1"): "green", ("A", "2"): "amber", ("A", "3"): "green", ("B", "1"): "green",
                   ("B", "2"): "amber", ("B", "3"): "green", ("C", "2"): "red"}


@pytest.mark.part2
def test_green_amber_red_by_margin(impl):
    curve = [pt(impl, 16, ttft=500, tps_user=100)]
    assert impl.verdict_for(curve, impl.SLA(16, 1000, 50)).color == "green"
    assert impl.verdict_for(curve, impl.SLA(16, 530, 50)).color == "amber"  # TTFT margin 5.7%
    assert impl.verdict_for(curve, impl.SLA(16, 1000, 95)).color == "amber"  # speed margin 5.3%
    red = impl.verdict_for(curve, impl.SLA(16, 400, 120))
    assert red.color == "red" and len(red.reasons) == 2  # both misses are named


@pytest.mark.part2
def test_uses_nearest_load_at_or_above(impl):
    curve = [pt(impl, 1, 100, 900), pt(impl, 4, 120, 800), pt(impl, 16, 200, 500), pt(impl, 64, 900, 100)]
    v = impl.verdict_for(curve, impl.SLA(10, 1000, 300))
    assert v.concurrency_used == 16 and v.color == "green"
    assert any("16" in r for r in v.reasons), "say which load was used"
    exact = impl.verdict_for(curve, impl.SLA(16, 1000, 300))
    assert exact.concurrency_used == 16 and exact.reasons == []


@pytest.mark.part2
def test_load_beyond_the_sweep_is_red(impl):
    curve = [pt(impl, 1, 100, 900), pt(impl, 4, 120, 800)]
    v = impl.verdict_for(curve, impl.SLA(64, 1000, 10))
    assert v.color == "red" and v.concurrency_used is None


@pytest.mark.part2
def test_anomaly_on_used_point_downgrades_green(impl):
    curve = [pt(impl, 16, 200, 500)]
    assert impl.verdict_for(curve, impl.SLA(16, 1000, 300), {16}).color == "amber"
    assert impl.verdict_for(curve, impl.SLA(16, 1000, 300), {4}).color == "green"


# ---------------------------------------------------------------- Part 3: anomalies


@pytest.mark.part3
def test_finds_exactly_the_planted_defects(impl):
    pts, _ = impl.load_all(FILES)
    got = sorted((a.model, a.profile, a.concurrency, a.kind) for a in impl.find_anomalies(pts))
    assert got == [("A", "2", 16, "ttft_drop"), ("B", "3", 64, "throughput_drop"), ("C", "2", 4, "total_mismatch")]


@pytest.mark.part3
def test_each_anomaly_kind(impl):
    good = [pt(impl, 1, 100, 900), pt(impl, 4, 120, 800), pt(impl, 16, 200, 500)]
    assert impl.find_anomalies(good) == []
    kinds = lambda pts: sorted(a.kind for a in impl.find_anomalies(pts))
    assert kinds(good[:2] + [pt(impl, 16, 200, 100)]) == ["throughput_drop"]  # 1600 < 3200
    assert kinds(good[:2] + [pt(impl, 16, 110, 500)]) == ["ttft_drop"]
    assert kinds(good[:2] + [pt(impl, 16, 200, 500, total=5000)]) == ["total_mismatch"]
    assert kinds(good[:2] + [pt(impl, 16, 200, 500, tpot=5.0)]) == ["tpot_mismatch"]
    assert kinds(good + [pt(impl, 16, 200, 500)]) == ["duplicate_point"]


@pytest.mark.part3
def test_small_wiggles_are_not_anomalies(impl):
    pts = [pt(impl, 1, 100, 900), pt(impl, 4, 99, 800, total=3150)]  # 1% faster TTFT, 1.6% off on total
    assert impl.find_anomalies(pts) == []


@pytest.mark.part3
def test_curves_are_kept_apart(impl):
    a = [pt(impl, 1, 100, 900, model="A"), pt(impl, 4, 120, 800, model="A")]
    b = [pt(impl, 1, 50, 900, model="B"), pt(impl, 4, 60, 800, model="B")]
    assert impl.find_anomalies(a + b) == []  # B's lower TTFT is not a drop on A's curve


# ---------------------------------------------------------------- Part 4: report


@pytest.mark.part4
def test_report_lists_every_curve_and_anomaly(impl, capsys):
    impl.main([str(f) for f in FILES] + ["--concurrency", "16", "--ttft-ms", "1400", "--tps-user", "300"])
    out = capsys.readouterr().out
    for word in ("green", "amber", "red", "ttft_drop", "throughput_drop", "total_mismatch", "missing_value"):
        assert word in out
    assert "C" in out and "3007" in out


# ---------------------------------------------------------------- edge cases


@pytest.mark.edge
def test_missing_required_column(impl, tmp_path):
    p = tmp_path / "Model_Z_profile_1.csv"
    p.write_text("isl,osl,concurrency,ttft_ms,tpot_ms,tok/s/user\n1,1,1,1,1,1\n")
    with pytest.raises(ValueError, match="tps_total"):
        impl.parse_sweep(p)


@pytest.mark.edge
def test_two_columns_for_one_field(impl):
    with pytest.raises(ValueError):
        impl.map_headers(["model", "profile", "isl", "osl", "concurrency", "ttft_ms", "ttft_s", "tpot", "tps_user",
                          "throughput"])


@pytest.mark.edge
def test_no_model_column_and_bad_file_name(impl, tmp_path):
    p = tmp_path / "sweep.csv"
    p.write_text("isl,osl,concurrency,ttft_ms,tpot_ms,tok/s/user,throughput\n1,1,1,1,1,1,1\n")
    with pytest.raises(ValueError):
        impl.parse_sweep(p)


@pytest.mark.edge
def test_non_numeric_cell_is_flagged_not_crashing(impl, tmp_path):
    p = tmp_path / "Model_Q_profile_3.csv"
    p.write_text("isl,osl,concurrency,ttft_ms,tpot_ms,tok/s/user,throughput\n"
                 "100,100,1,50,2,500,500\n100,100,4,n/a,2.2,450,1800\n")
    pts, an = impl.parse_sweep(p)
    assert len(pts) == 1 and [(a.concurrency, a.kind) for a in an] == [(4, "missing_value")]
