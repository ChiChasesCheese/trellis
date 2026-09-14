import random

import pytest

GLASSDOOR = ["ALLOCATE apibox", "ALLOCATE apibox", "ALLOCATE sitebox", "ALLOCATE apibox",
             "DEALLOCATE apibox2", "ALLOCATE apibox"]
GLASSDOOR_OUT = ["apibox1", "apibox2", "sitebox1", "apibox3", "apibox2"]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_stealthbomber10_gist_vectors_verbatim(impl):
    f = impl.next_server_number
    assert f([5, 3, 1]) == 2
    assert f([5, 4, 1, 2]) == 3
    assert f([3, 2, 1]) == 4
    assert f([2, 3]) == 1
    assert f([]) == 1
    assert f([1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 5.5]) == 6


@pytest.mark.part1
def test_aranibatta_gist_vectors_verbatim(impl):
    f = impl.next_server_number
    assert f([]) == 1
    assert f([5, 4, 1, 2]) == 3
    assert f([1, 2, 3, 4, 5]) == 6
    assert f([5, 4, 3, 2]) == 1
    assert f([1, 2, 3, 4, 6]) == 5


@pytest.mark.part1
@pytest.mark.edge
def test_next_number_ignores_dups_zero_negatives_and_order(impl):
    f = impl.next_server_number
    assert f([1, 1, 1]) == 2
    assert f([0, -1, -5]) == 1
    assert f([0, 1, 2]) == 3
    assert f([2, 1, 2, 1]) == 3
    assert f(range(1, 100_001)) == 100_001
    assert f([10**9]) == 1
    assert f((3, 1, 2)) == 4  # any iterable


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_tracker_verbatim(impl):
    t = impl.Tracker()
    assert t.allocate("apibox") == "apibox1"
    assert t.allocate("apibox") == "apibox2"
    assert t.deallocate("apibox1") is True
    assert t.allocate("apibox") == "apibox1"
    assert t.allocate("sitebox") == "sitebox1"


@pytest.mark.part2
def test_example_glassdoor_sequence(impl):
    assert impl.run_commands(GLASSDOOR) == GLASSDOOR_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_unknown_and_double_deallocate_ignored(impl):
    t = impl.Tracker()
    assert t.deallocate("apibox1") is False          # never allocated
    assert t.allocate("apibox") == "apibox1"
    assert t.deallocate("apibox1") is True
    assert t.deallocate("apibox1") is False          # already freed
    assert t.allocate("apibox") == "apibox1"
    assert t.allocate("apibox") == "apibox2"         # the double free did not create a second '1'
    for bad in ("apibox", "apibox0", "sitebox9", "", "apibox01", "12"):
        assert t.deallocate(bad) is False, bad
    assert t.allocate("apibox") == "apibox3"


@pytest.mark.part2
@pytest.mark.edge
def test_strict_mode_raises(impl):
    t = impl.Tracker(strict=True)
    with pytest.raises(KeyError):
        t.deallocate("apibox1")
    t.allocate("apibox")
    assert t.deallocate("apibox1") is True
    with pytest.raises(KeyError):
        t.deallocate("apibox1")


@pytest.mark.part2
@pytest.mark.edge
def test_freed_numbers_reused_ascending_then_high_water_mark(impl):
    t = impl.Tracker()
    names = [t.allocate("apibox") for _ in range(5)]
    assert names == ["apibox1", "apibox2", "apibox3", "apibox4", "apibox5"]
    t.deallocate("apibox3")
    t.deallocate("apibox1")
    t.deallocate("apibox4")
    assert [t.allocate("apibox") for _ in range(4)] == ["apibox1", "apibox3", "apibox4", "apibox6"]


@pytest.mark.part2
@pytest.mark.edge
def test_types_independent_and_multidigit_names(impl):
    t = impl.Tracker()
    for _ in range(12):
        t.allocate("apibox")
    assert t.allocate("sitebox") == "sitebox1"
    assert t.deallocate("apibox10") is True
    assert t.allocate("sitebox") == "sitebox2"      # apibox10 freed does not touch sitebox
    assert t.allocate("apibox") == "apibox10"
    assert t.deallocate("apibox12") is True
    assert t.allocate("apibox") == "apibox12"
    assert t.allocate("apibox") == "apibox13"
    assert impl.split_hostname("apibox12") == ("apibox", 12)
    assert impl.split_hostname("db-primary7") == ("db-primary", 7)
    assert impl.split_hostname("apibox") is None and impl.split_hostname("42") is None


@pytest.mark.part2
@pytest.mark.edge
def test_type_ending_in_digit_rejected(impl):
    t = impl.Tracker()
    with pytest.raises(ValueError):
        t.allocate("box2")
    with pytest.raises(ValueError):
        t.allocate("")
    assert t.allocate("box") == "box1"


# ---------------------------------------------------------------- Part 3 (complexity): behaviour under churn
@pytest.mark.part3
@pytest.mark.edge
def test_heavy_churn_matches_brute_force(impl):
    rng = random.Random(1)
    t = impl.Tracker()
    live = set()
    for _ in range(5000):
        if live and rng.random() < 0.45:
            name = rng.choice(sorted(live))
            assert t.deallocate(name) is True
            live.remove(name)
        else:
            typ = rng.choice(["apibox", "sitebox"])
            name = t.allocate(typ)
            # brute force: smallest number of that type not live
            nums = {int(n[len(typ):]) for n in live if n.startswith(typ)}
            assert name == f"{typ}{impl.next_server_number(nums)}"
            live.add(name)


@pytest.mark.part3
def test_many_frees_then_allocations_come_back_sorted(impl):
    t = impl.Tracker()
    for _ in range(1000):
        t.allocate("w")
    order = list(range(1, 1001))
    random.Random(2).shuffle(order)
    for n in order:
        t.deallocate(f"w{n}")
    assert [t.allocate("w") for _ in range(1000)] == [f"w{i}" for i in range(1, 1001)]
    assert t.allocate("w") == "w1001"


# ---------------------------------------------------------------- Part 4 / io / perf
@pytest.mark.part4
@pytest.mark.io
def test_stdin_commands_exact(run_script):
    r = run_script("PART 4\n" + "\n".join(GLASSDOOR) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(GLASSDOOR_OUT) + "\n"
    r = run_script("PART 2\nALLOCATE apibox\n\nDEALLOCATE nope\nDEALLOCATE apibox1\nALLOCATE apibox\n")
    assert r.stdout == "apibox1\napibox1\n"
    assert run_script("PART 4\nDEALLOCATE apibox1\n").stdout == ""
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.io
def test_stdin_part1_exact(run_script):
    r = run_script("PART 1\n5 3 1\n[]\n\n[3, 2, 1]\n1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 5.5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n1\n1\n4\n6\n"


@pytest.mark.part4
@pytest.mark.perf
def test_perf_one_million_commands(run_script):
    rng = random.Random(0)
    types = ["apibox", "sitebox", "dbbox", "cachebox"]
    lines, per_type, alive = ["PART 4"], {t: 0 for t in types}, []
    for _ in range(1_000_000):
        if alive and rng.random() < 0.4:
            i = rng.randrange(len(alive))
            alive[i], alive[-1] = alive[-1], alive[i]
            lines.append(f"DEALLOCATE {alive.pop()}")
        else:  # generator mirrors the allocator only loosely; names are valid, reuse is what the solution decides
            t = rng.choice(types)
            per_type[t] += 1
            alive.append(f"{t}{per_type[t]}")
            lines.append(f"ALLOCATE {t}")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == sum(1 for ln in lines if ln.startswith("ALLOCATE"))
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
