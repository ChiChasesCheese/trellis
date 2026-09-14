import random

import pytest

Q1 = ["A:d1", "B:d2", "C:d3", "D:d2", "B:d3"]
Q2 = ["A:d1:123", "B:d2:456", "C:d3:123", "D:d2:789", "E:d2:999"]
Q3 = ["A:d1:123:90", "B:d2:456:50", "C:d3:123:0", "D:d2:789:100", "E:d2:999:30"]
P4 = ["u1,alice smith,alice@x.com,acme", "u2,alice smith,other@x.com,acme",
      "u3,bob,alice@x.com,zzz", "u4,alice smith,,"]


# ---------------------------------------------------------------- Part 1: direct links
@pytest.mark.part1
def test_example_2_direct_links(impl):
    assert impl.direct_links(Q2, "A") == ["C"]
    assert impl.direct_links(Q2, "B") == ["D", "E"]


@pytest.mark.part1
def test_direct_links_q1_multi_record_customer(impl):
    # B has records with d2 and d3 -> linked to both C and D; A is alone
    assert impl.direct_links(Q1, "B") == ["C", "D"]
    assert impl.direct_links(Q1, "A") == []
    assert impl.direct_links(Q1, "C") == ["B"]  # not D: C-D is only transitive


@pytest.mark.part1
@pytest.mark.edge
def test_direct_links_dedup_and_excludes_self(impl):
    # A and B share both device and card -> listed once; A's two records don't list A
    assert impl.direct_links(["A:d1:c1", "B:d1:c1", "A:d9:c9"], "A") == ["B"]


@pytest.mark.part1
@pytest.mark.edge
def test_direct_links_unknown_target_empty_and_positions(impl):
    assert impl.direct_links(Q1, "Z") == []
    assert impl.direct_links([], "A") == []
    # same value at different positions never links; empty field links nothing
    assert impl.direct_links(["A:x:y", "B:y:x"], "A") == []
    assert impl.direct_links(["A::c1", "B::c2"], "A") == []
    assert impl.direct_links([" A : d1 ", "", "B:d1"], "A") == ["B"]


@pytest.mark.part1
@pytest.mark.fmt
def test_direct_links_sorted_plain_string_order(impl):
    recs = ["t:d", "b:d", "a:d", "B:d", "a10:d", "a2:d"]
    assert impl.direct_links(recs, "t") == ["B", "a", "a10", "a2", "b"]


# ---------------------------------------------------------------- Part 2: rings
@pytest.mark.part2
def test_example_1_groups(impl):
    assert impl.groups(Q1) == [{"A"}, {"B", "C", "D"}]
    assert impl.ring_size(Q1, "B") == 3
    assert impl.should_block(Q1, "B", 3) is True


@pytest.mark.part2
def test_example_2_largest_ring(impl):
    assert impl.groups(Q2) == [{"A", "C"}, {"B", "D", "E"}]
    assert impl.largest_ring(Q2) == 3
    assert impl.ring_size(Q2, "A") == 2 and impl.should_block(Q2, "A", 3) is False


@pytest.mark.part2
@pytest.mark.edge
def test_block_threshold_boundary(impl):
    assert impl.should_block(Q1, "B", 2) is True   # 3 >= 2
    assert impl.should_block(Q1, "B", 3) is True   # == K blocks
    assert impl.should_block(Q1, "B", 4) is False  # one above
    assert impl.should_block(Q1, "A", 1) is True   # lone customer has ring size 1


@pytest.mark.part2
@pytest.mark.edge
def test_ring_size_self_unknown_empty(impl):
    assert impl.ring_size(Q1, "A") == 1
    assert impl.ring_size(Q1, "zzz") == 0
    assert impl.largest_ring([]) == 0 and impl.groups([]) == []


@pytest.mark.part2
@pytest.mark.edge
def test_long_chain_is_one_ring_regardless_of_order(impl):
    chain = ["E:d4", "A:d1", "C:d2:x", "D:d3", "B:d1", "B:d2", "C:d3", "D:d4"]
    assert impl.ring_size(chain, "A") == 5
    assert impl.largest_ring(chain) == 5
    assert impl.groups(chain) == [{"A", "B", "C", "D", "E"}]


@pytest.mark.part2
@pytest.mark.edge
def test_card_only_link_and_duplicate_records(impl):
    recs = ["A:d1:c1", "A:d1:c1", "B:d2:c1", "C:d3:c3", "C:d3:c3"]
    assert impl.groups(recs) == [{"A", "B"}, {"C"}]
    assert impl.ring_size(recs, "A") == 2


# ---------------------------------------------------------------- Part 3: risk
@pytest.mark.part3
def test_example_3_ring_risks(impl):
    assert impl.ring_risks(Q3) == [90, 60]


@pytest.mark.part3
@pytest.mark.edge
def test_all_zero_ring_scores_zero_and_last_record_wins(impl):
    assert impl.ring_risks(["A:d1:c1:0", "B:d1:c2:0", "C:d9:c9:40"]) == [0, 40]
    # A's risk is updated by its later record (90 -> 10)
    assert impl.ring_risks(["A:d1:c1:90", "B:d1:c2:50", "A:d1:c1:10"]) == [30]


@pytest.mark.part3
@pytest.mark.fmt
def test_risk_mean_non_integer_two_decimals(run_script):
    r = run_script("PART 3\nA:d1:c1:1\nB:d1:c2:2\nC:d1:c3:0\nZ:d0:c0:7\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "A,B,C 1.50\nZ 7.00\n"


@pytest.mark.part3
@pytest.mark.edge
def test_risk_ring_order_is_first_appearance(impl):
    recs = ["Z:d1:c1:10", "A:d2:c2:20", "Y:d1:c3:30"]
    assert impl.ring_risks(recs) == [20, 20]
    assert impl.groups([":".join(r.split(":")[:-1]) for r in recs]) == [{"Z", "Y"}, {"A"}]


# ---------------------------------------------------------------- Part 4: weighted
@pytest.mark.part4
def test_example_4_weighted(impl):
    assert impl.weighted_links(P4, "u1") == ["u2", "u3"]


@pytest.mark.part4
@pytest.mark.edge
def test_weighted_threshold_float_safe_and_boundary(impl):
    # name .2 + company .3 = .5 exactly -> linked at 0.5, not at 0.51
    assert impl.weighted_links(P4, "u1", threshold=0.5) == ["u2", "u3"]
    assert impl.weighted_links(P4, "u1", threshold=0.51) == []           # one above: u3 is exactly .5 too
    assert impl.weighted_links(P4, "u1", threshold=0.49) == ["u2", "u3"]
    assert impl.weighted_links(P4, "u1", threshold=0.2) == ["u2", "u3", "u4"]
    assert impl.weighted_links(P4, "u1", threshold=1.0) == []


@pytest.mark.part4
@pytest.mark.edge
def test_weighted_case_insensitive_empty_fields_custom_weights(impl):
    recs = ["a,Alice,ALICE@X.COM,Acme", "b,alice,alice@x.com,acme", "c,,,", "d,,alice@x.com,"]
    assert impl.weighted_links(recs, "a") == ["b", "d"]
    assert impl.weighted_links(recs, "c") == []  # empty fields never match, even both empty
    assert impl.weighted_links(recs, "a", weights={"name": 1.0, "email": 0.0, "company": 0.0}) == ["b"]
    assert impl.weighted_links(recs, "ghost") == []


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_part1_and_none(run_script):
    r = run_script("PART 1\nB\n" + "\n".join(Q2) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "D\nE\n"
    r = run_script("PART 1\nA\n" + "\n".join(Q1) + "\n")
    assert r.stdout == "NONE\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_part2_part4(run_script):
    assert run_script("PART 2\nB 3\n" + "\n".join(Q1) + "\n").stdout == "3 BLOCK\n"
    assert run_script("PART 2\nA 3\n" + "\n".join(Q2) + "\n").stdout == "2 ALLOW\n"
    assert run_script("PART 4\nu1 0.5\n" + "\n".join(P4) + "\n").stdout == "u2\nu3\n"
    assert run_script("PART 4\nu4 0.9\n" + "\n".join(P4) + "\n").stdout == "NONE\n"
    assert run_script("").stdout == ""


@pytest.mark.part3
@pytest.mark.io
def test_stdin_part3_exact(run_script):
    r = run_script("PART 3\n" + "\n".join(Q3) + "\n")
    assert r.stdout == "A,C 90.00\nB,D,E 60.00\n"


@pytest.mark.part2
@pytest.mark.perf
def test_perf_100k_records(run_script):
    rng = random.Random(0)
    lines = [f"c{rng.randrange(50_000)}:d{rng.randrange(40_000)}:k{rng.randrange(40_000)}:{rng.randrange(101)}"
             for _ in range(100_000)]
    r = run_script("PART 3\n" + "\n".join(lines) + "\n", timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") >= 1
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
