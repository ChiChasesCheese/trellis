import random

import pytest

WEIGHTS = {"name": 0.2, "email": 0.5, "company": 0.3}
THRESHOLD = 0.5

# Verbatim-equivalent worked example from PracHub ("find-linked-user-records-by-similarity"):
# record 1/2 share email+company (0.8 >= 0.5) -> linked; nothing else reaches threshold.
REAL_ROWS = [
    {"id": "1", "name": "Alice", "email": "alice@gmail.com", "company": "Stripe"},
    {"id": "2", "name": "Alicia", "email": "alice@gmail.com", "company": "Stripe"},
    {"id": "3", "name": "Alice", "email": "alice@yahoo.com", "company": "Google"},
    {"id": "4", "name": "Bob", "email": "bob@gmail.com", "company": "Stripe"},
]

# Self-authored chain (this repo — see problem.md Sources): 1-2 (name+company=0.5), 2-3
# (email=0.5), 3-4 (name+company=0.5); 1-3, 1-4, 2-4 all score 0; record 5 is isolated. This is
# the smallest example that actually distinguishes Part 1 / Part 2 / Part 3 from each other.
CHAIN_ROWS = [
    {"id": "1", "name": "Alice", "email": "alice1@co.com", "company": "Acme"},
    {"id": "2", "name": "Alice", "email": "alice2@co.com", "company": "Acme"},
    {"id": "3", "name": "Zed", "email": "alice2@co.com", "company": "Zenith"},
    {"id": "4", "name": "Zed", "email": "zed4@co.com", "company": "Zenith"},
    {"id": "5", "name": "Bob", "email": "bob5@co.com", "company": "Other"},
]

HEADER = "id,name,email,company"


def _stdin(part: int, target: str, rows: list[dict], weights=WEIGHTS, threshold=THRESHOLD) -> str:
    weight_line = ",".join(f"{f}={w}" for f, w in weights.items())
    lines = [f"PART {part}", target, str(threshold), weight_line, HEADER]
    lines += [f"{r['id']},{r['name']},{r['email']},{r['company']}" for r in rows]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- Part 1: direct links
@pytest.mark.part1
def test_real_example_direct_link(impl):
    assert impl.part1(REAL_ROWS, WEIGHTS, THRESHOLD, "1") == ["2"]


@pytest.mark.part1
def test_chain_example_direct_link(impl):
    assert impl.part1(CHAIN_ROWS, WEIGHTS, THRESHOLD, "1") == ["2"]


@pytest.mark.part1
def test_no_links_returns_empty(impl):
    assert impl.part1(REAL_ROWS, WEIGHTS, THRESHOLD, "4") == []


@pytest.mark.part1
@pytest.mark.edge
def test_threshold_boundary_exact_score_counts_as_linked(impl):
    # email match alone = 0.5 == threshold -> linked (non-strict >=)
    rows = [
        {"id": "a", "name": "X", "email": "shared@x.com", "company": "Foo"},
        {"id": "b", "name": "Y", "email": "shared@x.com", "company": "Bar"},
    ]
    assert impl.part1(rows, WEIGHTS, THRESHOLD, "a") == ["b"]


@pytest.mark.part1
@pytest.mark.edge
def test_both_fields_empty_never_counts_as_a_match(impl):
    # if empty==empty were (wrongly) counted, name(0.2)+company(0.3)=0.5 would cross threshold
    rows = [
        {"id": "a", "name": "X", "email": "e1@x.com", "company": ""},
        {"id": "b", "name": "X", "email": "e2@x.com", "company": ""},
    ]
    assert impl.part1(rows, WEIGHTS, THRESHOLD, "a") == []


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_record_id_raises(impl):
    rows = REAL_ROWS + [{"id": "1", "name": "Dup", "email": "x@x.com", "company": "X"}]
    with pytest.raises(ValueError):
        impl.part1(rows, WEIGHTS, THRESHOLD, "1")


@pytest.mark.part1
@pytest.mark.edge
def test_unknown_target_user_id_raises(impl):
    with pytest.raises(ValueError):
        impl.part1(REAL_ROWS, WEIGHTS, THRESHOLD, "does-not-exist")


@pytest.mark.part1
@pytest.mark.fmt
def test_result_sorted_as_plain_strings_not_numerically(impl):
    # 'u10' < 'u2' in plain string order even though 10 > 2 numerically
    rows = [
        {"id": "target", "name": "N", "email": "shared@x.com", "company": "C1"},
        {"id": "u2", "name": "A", "email": "shared@x.com", "company": "C2"},
        {"id": "u10", "name": "B", "email": "shared@x.com", "company": "C3"},
    ]
    assert impl.part1(rows, WEIGHTS, THRESHOLD, "target") == ["u10", "u2"]


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script(_stdin(1, "1", REAL_ROWS))
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n"


# ---------------------------------------------------------------- Part 2: <= 2 hops
@pytest.mark.part2
def test_real_example_two_hop_matches_reported_quirk(impl):
    # PracHub's own reported Part 2 output on this exact record set is also [2] -- with only 4
    # records and no 2-hop-only member, Part 1 and Part 2 coincide here (see problem.md Sources).
    assert impl.part2(REAL_ROWS, WEIGHTS, THRESHOLD, "1") == ["2"]


@pytest.mark.part2
def test_chain_example_two_hop_reaches_indirect_neighbor(impl):
    # 1's only direct link is 2; 2's direct links are {1, 3} -> within 2 hops: {2, 3}
    assert impl.part2(CHAIN_ROWS, WEIGHTS, THRESHOLD, "1") == ["2", "3"]


@pytest.mark.part2
def test_two_hop_does_not_reach_third_hop(impl):
    # 4 is 3 hops from 1 (1-2-3-4) -> must NOT appear in Part 2's <= 2 hop result
    out = impl.part2(CHAIN_ROWS, WEIGHTS, THRESHOLD, "1")
    assert "4" not in out


@pytest.mark.part2
@pytest.mark.edge
def test_isolated_target_has_no_two_hop_links(impl):
    assert impl.part2(CHAIN_ROWS, WEIGHTS, THRESHOLD, "5") == []


@pytest.mark.part2
@pytest.mark.edge
def test_triangle_does_not_duplicate_or_crash(impl):
    rows = [
        {"id": "a", "name": "N", "email": "e@x.com", "company": "C"},
        {"id": "b", "name": "N", "email": "e@x.com", "company": "C"},
        {"id": "c", "name": "N", "email": "e@x.com", "company": "C"},
    ]
    assert impl.part2(rows, WEIGHTS, THRESHOLD, "a") == ["b", "c"]


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script(_stdin(2, "1", CHAIN_ROWS))
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2,3\n"


# ---------------------------------------------------------------- Part 3: full component
@pytest.mark.part3
def test_chain_example_full_component(impl):
    assert impl.part3(CHAIN_ROWS, WEIGHTS, THRESHOLD, "1") == ["2", "3", "4"]


@pytest.mark.part3
def test_real_example_full_component(impl):
    assert impl.part3(REAL_ROWS, WEIGHTS, THRESHOLD, "1") == ["2"]


@pytest.mark.part3
def test_isolated_record_component_is_empty(impl):
    assert impl.part3(CHAIN_ROWS, WEIGHTS, THRESHOLD, "5") == []


@pytest.mark.part3
@pytest.mark.edge
def test_triangle_component_no_duplicates(impl):
    rows = [
        {"id": "a", "name": "N", "email": "e@x.com", "company": "C"},
        {"id": "b", "name": "N", "email": "e@x.com", "company": "C"},
        {"id": "c", "name": "N", "email": "e@x.com", "company": "C"},
    ]
    assert impl.part3(rows, WEIGHTS, THRESHOLD, "a") == ["b", "c"]


@pytest.mark.part3
@pytest.mark.edge
def test_component_can_include_records_unreachable_within_two_hops(impl):
    out = impl.part3(CHAIN_ROWS, WEIGHTS, THRESHOLD, "1")
    assert "4" in out  # 3 hops away, excluded from Part 2's result but included here


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3_none_when_no_links(run_script):
    r = run_script(_stdin(3, "5", CHAIN_ROWS))
    assert r.returncode == 0, r.stderr
    assert r.stdout == "NONE\n"


@pytest.mark.part3
@pytest.mark.perf
def test_perf_large_number_of_isolated_components(run_script):
    rng = random.Random(0)
    n = 6000
    n_clusters = 150
    cluster_size = n // n_clusters  # 40
    lines = ["PART 3", "u0", str(THRESHOLD), "name=0.2,email=0.5,company=0.3", HEADER]
    ids = [f"u{i}" for i in range(n)]
    rng.shuffle(ids)  # input order shouldn't matter
    for rid in ids:
        cluster = int(rid[1:]) % n_clusters
        lines.append(f"{rid},N{cluster},E{cluster}@x.com,C{cluster}")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    out = r.stdout.strip()
    assert out != "NONE"
    assert len(out.split(",")) == cluster_size - 1  # whole cluster minus the target itself
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
