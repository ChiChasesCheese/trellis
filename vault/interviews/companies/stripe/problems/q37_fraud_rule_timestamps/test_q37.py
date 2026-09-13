import random

import pytest

EX1 = ["RULE,burgers,100,merchant=bobs_burgers", "AUTH,a1,50,bobs_burgers,1200",
       "AUTH,a2,100,bobs_burgers,1200", "AUTH,a3,150,alice_cafe,1200"]
EX1_OUT = ["50,a1,1200,APPROVE", "100,a2,1200,REJECT", "150,a3,1200,APPROVE"]
EX2 = ["RULE,big,0,amount>1000", "RULE,big,300,amount>5000", "RULE,big,400,none",
       "RULE,burgers,100,merchant=bobs_burgers", "AUTH,b1,250,shop,2000", "AUTH,b2,300,shop,2000",
       "AUTH,b3,300,shop,6000", "AUTH,b4,400,shop,6000", "AUTH,b5,400,bobs_burgers,1"]
EX2_OUT = ["250,b1,2000,REJECT", "300,b2,2000,APPROVE", "300,b3,6000,REJECT",
           "400,b4,6000,APPROVE", "400,b5,1,REJECT"]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_single_rule(impl):
    assert impl.process(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_effective_from_boundary(impl):
    rule = "RULE,r,100,merchant=m"
    assert impl.process([rule, "AUTH,x,99,m,1"]) == ["99,x,1,APPROVE"]
    assert impl.process([rule, "AUTH,x,100,m,1"]) == ["100,x,1,REJECT"]
    assert impl.process([rule, "AUTH,x,101,m,1"]) == ["101,x,1,REJECT"]


@pytest.mark.part1
@pytest.mark.edge
def test_no_rules_or_no_requests(impl):
    assert impl.process(["AUTH,x,5,m,1"]) == ["5,x,1,APPROVE"]
    assert impl.process(["RULE,r,0,merchant=m"]) == []
    assert impl.process([]) == []


@pytest.mark.part1
def test_matches_operators(impl):
    a = impl.Auth("id", 0, "shop", 900)
    assert impl.matches("merchant=shop", a) and not impl.matches("merchant=other", a)
    assert impl.matches("merchant!=other", a) and not impl.matches("merchant!=shop", a)
    assert not impl.matches("amount>1000", a) and impl.matches("amount>=900", a)
    assert impl.matches("amount<=900", a) and not impl.matches("amount<900", a)
    assert not impl.matches("none", a)


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_versions(impl):
    assert impl.process(EX2) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_only_version_in_force_is_evaluated(impl):
    lines = ["RULE,r,0,merchant=a", "RULE,r,10,merchant=b"]
    # at t=10 version 2 (merchant=b) is in force: 'a' no longer rejected, 'b' is
    assert impl.process(lines + ["AUTH,x,10,a,1", "AUTH,y,10,b,1", "AUTH,z,9,b,1"]) == [
        "9,z,1,APPROVE", "10,x,1,APPROVE", "10,y,1,REJECT"]


@pytest.mark.part2
@pytest.mark.edge
def test_same_effective_from_later_line_wins_and_any_rule_rejects(impl):
    lines = ["RULE,r,0,merchant=a", "RULE,r,0,merchant=b", "RULE,s,0,amount>=5"]
    assert impl.process(lines + ["AUTH,x,0,a,1", "AUTH,y,0,b,1", "AUTH,z,0,c,5"]) == [
        "0,x,1,APPROVE", "0,y,1,REJECT", "0,z,5,REJECT"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_expiry(impl):
    out = impl.process(["RULE,promo,100,200,merchant=bobs_burgers", "AUTH,c1,199,bobs_burgers,10",
                        "AUTH,c2,200,bobs_burgers,10"])
    assert out == ["199,c1,10,REJECT", "200,c2,10,APPROVE"]


@pytest.mark.part3
@pytest.mark.edge
def test_expiry_boundaries_and_no_fallback(impl):
    lines = ["RULE,r,0,merchant=m", "RULE,r,10,20,merchant=m"]
    got = impl.process(lines + [f"AUTH,t{t:02d},{t},m,1" for t in (9, 10, 19, 20, 21)])
    assert got == ["9,t09,1,REJECT", "10,t10,1,REJECT", "19,t19,1,REJECT",
                   "20,t20,1,APPROVE", "21,t21,1,APPROVE"]  # expired v2 does not revive v1


@pytest.mark.part3
@pytest.mark.edge
def test_expiry_then_newer_version(impl):
    lines = ["RULE,r,0,5,merchant=m", "RULE,r,50,merchant=m"]
    assert impl.process(lines + ["AUTH,a,5,m,1", "AUTH,b,50,m,1"]) == ["5,a,1,APPROVE", "50,b,1,REJECT"]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example_out_of_order(impl):
    out = impl.process(["AUTH,d2,10,shop,900", "RULE,late,0,amount>=900", "AUTH,d1,10,shop,899"])
    assert out == ["10,d1,899,APPROVE", "10,d2,900,REJECT"]


@pytest.mark.part4
@pytest.mark.fmt
def test_output_sorted_by_timestamp_then_id_string_order(impl):
    out = impl.process(["AUTH,a2,5,m,1", "AUTH,a10,5,m,1", "AUTH,b,4,m,1", "RULE,r,100,merchant=m"])
    assert out == ["4,b,1,APPROVE", "5,a10,1,APPROVE", "5,a2,1,APPROVE"]


@pytest.mark.part4
@pytest.mark.edge
def test_versions_ordered_by_effective_from_not_line_order(impl):
    lines = ["RULE,r,10,merchant=b", "RULE,r,0,merchant=a"]   # v(0) listed after v(10)
    assert impl.process(lines + ["AUTH,x,5,a,1", "AUTH,y,15,a,1"]) == ["5,x,1,REJECT", "15,y,1,APPROVE"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("\n".join(EX2) + "\n\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX2_OUT) + "\n"
    assert run_script("").stdout == ""


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_auths_50_rules(run_script):
    rng = random.Random(0)
    lines = []
    for r in range(50):
        for v in range(4):
            cond = rng.choice([f"merchant=m{rng.randrange(100)}", f"amount>{rng.randrange(100000)}", "none"])
            lines.append(f"RULE,r{r},{rng.randrange(1_000_000)},{cond}")
    for i in range(100_000):
        lines.append(f"AUTH,x{i},{rng.randrange(1_000_000)},m{rng.randrange(100)},{rng.randrange(100000)}")
    rng.shuffle(lines)
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 100_000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
