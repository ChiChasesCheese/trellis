import random
import sys

import pytest


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_order(impl):
    out = impl.part1(
        ["BIRTH rhea zoe", "BIRTH rhea amy", "BIRTH zoe leo", "ORDER", "DEATH zoe", "ORDER"]
    )
    assert out == ["rhea zoe leo amy", "rhea leo amy"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_family_order_is_dash(impl):
    assert impl.part1(["ORDER"]) == ["-"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_family_via_object_is_empty_list(impl):
    t = impl.ThroneInheritance()
    assert t.get_inheritance_order() == []


@pytest.mark.part1
@pytest.mark.edge
def test_first_birth_establishes_founder(impl):
    t = impl.ThroneInheritance()
    t.birth("rhea", "zoe")
    assert t.get_inheritance_order() == ["rhea", "zoe"]


@pytest.mark.part1
@pytest.mark.edge
def test_siblings_in_birth_order_not_alphabetical(impl):
    t = impl.ThroneInheritance()
    t.birth("rhea", "zoe")
    t.birth("rhea", "amy")  # "amy" < "zoe" alphabetically, but born second
    assert t.get_inheritance_order() == ["rhea", "zoe", "amy"]


@pytest.mark.part1
@pytest.mark.edge
def test_self_parent_raises_and_does_not_establish_founder(impl):
    t = impl.ThroneInheritance()
    with pytest.raises(ValueError):
        t.birth("rhea", "rhea")
    assert t.get_inheritance_order() == []  # founder was never planted


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_child_name_raises(impl):
    t = impl.ThroneInheritance()
    t.birth("rhea", "zoe")
    with pytest.raises(ValueError):
        t.birth("amy", "zoe")  # zoe already exists, no matter who claims to be the parent
    with pytest.raises(ValueError):
        t.birth("zoe", "rhea")  # rhea (the founder) already exists too


@pytest.mark.part1
@pytest.mark.edge
def test_unknown_parent_raises_once_founder_exists(impl):
    t = impl.ThroneInheritance()
    t.birth("rhea", "zoe")
    with pytest.raises(ValueError):
        t.birth("ghost", "leo")


@pytest.mark.part1
def test_command_stream_errors(impl):
    out = impl.part1(["BIRTH rhea zoe", "BIRTH amy zoe", "BIRTH ghost leo", "BIRTH rhea rhea"])
    assert out == ["ERROR", "ERROR", "ERROR"]


@pytest.mark.part1
@pytest.mark.edge
def test_death_is_idempotent_on_living_dead_and_unknown(impl):
    t = impl.ThroneInheritance()
    t.birth("rhea", "zoe")
    t.death("zoe")
    t.death("zoe")  # already dead: no error, no change
    t.death("ghost")  # never born: no error, no-op
    assert t.get_inheritance_order() == ["rhea"]


@pytest.mark.part1
@pytest.mark.edge
def test_dead_branch_keeps_living_descendants(impl):
    t = impl.ThroneInheritance()
    t.birth("rhea", "zoe")
    t.birth("zoe", "leo")
    t.death("zoe")
    assert t.get_inheritance_order() == ["rhea", "leo"]


@pytest.mark.part1
@pytest.mark.edge
def test_dead_person_can_still_have_new_children(impl):
    t = impl.ThroneInheritance()
    t.birth("rhea", "zoe")
    t.death("zoe")
    t.birth("zoe", "leo")  # zoe is dead but still in the tree; this must not raise
    assert t.get_inheritance_order() == ["rhea", "leo"]


@pytest.mark.part1
@pytest.mark.edge
def test_dead_founder_still_anchors_the_order(impl):
    t = impl.ThroneInheritance()
    t.birth("rhea", "zoe")
    t.death("rhea")
    assert t.get_inheritance_order() == ["zoe"]


# ------------------------------------------------------------------------ Part 2 (iterative)
@pytest.mark.part2
@pytest.mark.perf
def test_order_and_succession_are_iterative_on_a_100000_deep_chain(impl):
    t = impl.ThroneInheritance()
    n = 100_000
    t.birth("n0", "n1")
    for i in range(1, n):
        t.birth(f"n{i}", f"n{i + 1}")

    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(150)  # a recursive DFS on this chain would blow this immediately
    try:
        order = t.get_inheritance_order()
        succ = t.succession_after("n0")
    finally:
        sys.setrecursionlimit(old_limit)

    assert len(order) == n + 1
    assert order[0] == "n0" and order[-1] == f"n{n}"
    assert succ == "n1"


@pytest.mark.part2
@pytest.mark.perf
def test_perf_100000_deep_chain_via_script(run_script):
    n = 100_000
    lines = ["BIRTH n0 n1"] + [f"BIRTH n{i} n{i + 1}" for i in range(1, n)] + ["ORDER"]
    r = run_script("PART 2\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    out_line = r.stdout.strip()
    assert out_line.split()[0] == "n0"
    assert out_line.split()[-1] == f"n{n}"
    assert r.seconds < 3.0, f"took {r.seconds:.2f}s"


@pytest.mark.part2
@pytest.mark.edge
def test_random_cross_check_against_naive_recursive_oracle(impl):
    """Replay the same random birth/death/order script against the solution and against a plain
    recursive DFS over a parallel mirror; they must always agree. Trees are kept shallow enough
    (<= ~40 deep) that the recursive oracle itself never overflows -- Part2's dedicated deep-chain
    tests above are what prove the iterative requirement."""

    def naive_order(children: dict, dead: set, founder):
        if founder is None:
            return []
        out: list[str] = []

        def dfs(node):
            if node not in dead:
                out.append(node)
            for c in children.get(node, []):
                dfs(c)

        dfs(founder)
        return out

    rng = random.Random(0)
    for trial in range(30):
        t = impl.ThroneInheritance()
        mirror_children: dict[str, list[str]] = {}
        mirror_dead: set[str] = set()
        founder = None
        names = [f"m{i}" for i in range(80)]
        rng.shuffle(names)
        born: list[str] = []

        for _ in range(150):
            action = rng.choice(["birth", "death", "order"])
            if action == "birth" and len(born) < len(names):
                unborn = [nm for nm in names if nm not in born]
                child = rng.choice(unborn)
                if founder is None:
                    parent = rng.choice(names)  # any name may found the family
                    if parent == child:
                        continue  # skip the deliberately-invalid self-parent case here
                    t.birth(parent, child)
                    mirror_children.setdefault(parent, []).append(child)
                    mirror_children.setdefault(child, [])
                    founder = parent
                    born += [parent, child]
                elif born:
                    parent = rng.choice(born)
                    t.birth(parent, child)
                    mirror_children.setdefault(parent, []).append(child)
                    mirror_children.setdefault(child, [])
                    born.append(child)
            elif action == "death" and born:
                name = rng.choice(born)
                t.death(name)
                mirror_dead.add(name)
            else:
                expected = naive_order(mirror_children, mirror_dead, founder)
                assert t.get_inheritance_order() == expected, f"trial {trial}"


# ------------------------------------------------------------------------ Part 3 (succession)
@pytest.mark.part3
def test_worked_example_succession(impl):
    out = impl.part3(
        [
            "BIRTH rhea zoe",
            "BIRTH rhea amy",
            "BIRTH zoe leo",
            "SUCCESSOR rhea",
            "SUCCESSOR zoe",
            "DEATH zoe",
            "SUCCESSOR rhea",
            "SUCCESSOR zoe",
            "SUCCESSOR amy",
            "SUCCESSOR ghost",
        ]
    )
    assert out == ["zoe", "leo", "leo", "leo", "-", "-"]


@pytest.mark.part3
@pytest.mark.edge
def test_succession_after_unknown_name_is_empty_string(impl):
    t = impl.ThroneInheritance()
    t.birth("rhea", "zoe")
    assert t.succession_after("ghost") == ""


@pytest.mark.part3
@pytest.mark.edge
def test_succession_after_last_person_is_empty_string(impl):
    t = impl.ThroneInheritance()
    t.birth("rhea", "zoe")
    assert t.succession_after("zoe") == ""


@pytest.mark.part3
@pytest.mark.edge
def test_succession_after_on_empty_family(impl):
    t = impl.ThroneInheritance()
    assert t.succession_after("anyone") == ""


@pytest.mark.part3
@pytest.mark.edge
def test_succession_after_dead_person_still_answers(impl):
    """The whole point of succession_after: you can ask 'who succeeds right after X died' even
    though X no longer shows up in get_inheritance_order()."""
    t = impl.ThroneInheritance()
    t.birth("rhea", "zoe")
    t.birth("zoe", "leo")
    t.death("zoe")
    assert "zoe" not in t.get_inheritance_order()
    assert t.succession_after("zoe") == "leo"


@pytest.mark.part3
@pytest.mark.edge
def test_succession_after_skips_multiple_consecutive_dead(impl):
    t = impl.ThroneInheritance()
    t.birth("rhea", "zoe")
    t.birth("zoe", "leo")
    t.birth("leo", "tom")
    t.death("zoe")
    t.death("leo")
    assert t.succession_after("rhea") == "tom"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nBIRTH rhea zoe\nBIRTH rhea amy\nBIRTH zoe leo\nORDER\nDEATH zoe\nORDER\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "rhea zoe leo amy\nrhea leo amy\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script(
        "PART 3\nBIRTH rhea zoe\nBIRTH rhea amy\nBIRTH zoe leo\nDEATH zoe\nSUCCESSOR rhea\nSUCCESSOR amy\n"
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout == "leo\n-\n"
