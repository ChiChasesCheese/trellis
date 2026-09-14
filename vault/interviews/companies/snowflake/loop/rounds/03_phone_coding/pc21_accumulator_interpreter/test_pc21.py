import random

import pytest

MOD = 1_000_000_007


def _trunc_div_ref(a, b):
    """Independent truncate-toward-zero division (values here stay well within float
    precision, so plain float division + int() truncation is a safe independent check)."""
    return int(a / b)


def _brute_calculator(commands):
    acc = 0
    for stmt in commands:
        op, n = stmt.split()
        n = int(n)
        if op == "ADD":
            acc += n
        elif op == "SUB":
            acc -= n
        elif op == "MULT":
            acc *= n
        elif op == "DIV":
            acc = _trunc_div_ref(acc, n)
    return acc


def _parse_snowcal(lines):
    funcs, top_level = {}, []
    i, n = 0, len(lines)
    while i < n:
        parts = lines[i].split()
        if parts[0] == "FUN":
            name = parts[1]
            body = []
            i += 1
            while lines[i] != "END":
                body.append(lines[i])
                i += 1
            funcs[name] = body
            i += 1
        else:
            top_level.append(lines[i])
            i += 1
    return top_level, funcs


def _brute_snowcal_mod(lines, count_cap=3000):
    """Independent SnowCal-with-REPEAT evaluator that just loops `count` times (no affine-map
    algebra at all) -- used to cross-check run_snowcal_mod for small counts."""
    top_level, funcs = _parse_snowcal(lines)

    def run(stmt, x, chain):
        parts = stmt.split()
        op = parts[0]
        if op == "ADD":
            return (x + int(parts[1])) % MOD
        if op == "MUL":
            return (x * int(parts[1])) % MOD
        if op == "INV":
            name = parts[1]
            if name not in funcs:
                raise ValueError(f"undefined {name}")
            if name in chain:
                raise ValueError(f"cycle at {name}")
            for inner in funcs[name]:
                x = run(inner, x, chain | {name})
            return x
        if op == "REPEAT":
            count, name = int(parts[1]), parts[2]
            if count > count_cap:
                raise OverflowError("count too large for the brute reference")
            for _ in range(count):
                x = run(f"INV {name}", x, chain)
            return x
        raise ValueError(f"unknown {stmt}")

    x = 0
    for stmt in top_level:
        x = run(stmt, x, frozenset())
    return x


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example(impl):
    assert impl.run_calculator(["ADD 6", "SUB 3", "MULT 4", "DIV 2"]) == 6


@pytest.mark.part1
@pytest.mark.edge
def test_div_truncates_toward_zero_negative(impl):
    assert impl.run_calculator(["SUB 7", "DIV 2"]) == -3  # -7 truncated (not floored: -4)
    assert impl.run_calculator(["ADD 7", "DIV 2"]) == 3


@pytest.mark.part1
@pytest.mark.edge
def test_div_by_zero_raises(impl):
    with pytest.raises(ValueError):
        impl.run_calculator(["ADD 5", "DIV 0"])


@pytest.mark.part1
@pytest.mark.edge
def test_empty_program(impl):
    assert impl.run_calculator([]) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_unknown_command_raises(impl):
    with pytest.raises(ValueError):
        impl.run_calculator(["FOO 3"])


@pytest.mark.part1
@pytest.mark.edge
def test_calculator_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(300):
        length = rng.randint(0, 12)
        commands = []
        for _ in range(length):
            op = rng.choice(["ADD", "SUB", "MULT", "DIV"])
            n = rng.choice([n for n in range(-9, 10) if not (op == "DIV" and n == 0)])
            commands.append(f"{op} {n}")
        assert impl.run_calculator(commands) == _brute_calculator(commands), commands


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_snowcal_worked_example(impl):
    prog = ["ADD 3", "FUN double", "MUL 2", "END", "INV double"]
    assert impl.run_snowcal(prog) == 6


@pytest.mark.part2
@pytest.mark.edge
def test_snowcal_functions_can_call_other_functions(impl):
    prog = [
        "FUN add_one", "ADD 1", "END",
        "FUN add_two", "INV add_one", "INV add_one", "END",
        "INV add_two", "INV add_two",
    ]
    assert impl.run_snowcal(prog) == 4


@pytest.mark.part2
@pytest.mark.edge
def test_snowcal_undefined_function_raises(impl):
    with pytest.raises(ValueError):
        impl.run_snowcal(["INV nope"])


@pytest.mark.part2
@pytest.mark.edge
def test_snowcal_direct_self_recursion_raises(impl):
    with pytest.raises(ValueError):
        impl.run_snowcal(["FUN loop", "INV loop", "END", "INV loop"])


@pytest.mark.part2
@pytest.mark.edge
def test_snowcal_mutual_recursion_raises(impl):
    prog = ["FUN a", "INV b", "END", "FUN b", "INV a", "END", "INV a"]
    with pytest.raises(ValueError):
        impl.run_snowcal(prog)


@pytest.mark.part2
@pytest.mark.edge
def test_snowcal_declaring_without_invoking_is_a_no_op(impl):
    prog = ["ADD 5", "FUN unused", "MUL 100", "END", "ADD 1"]
    assert impl.run_snowcal(prog) == 6


@pytest.mark.part2
@pytest.mark.edge
def test_snowcal_against_random_acyclic_programs(impl):
    rng = random.Random(1)
    for _ in range(150):
        num_funcs = rng.randint(1, 4)
        names = [f"f{i}" for i in range(num_funcs)]
        funcs_src = []
        for i, name in enumerate(names):
            body_len = rng.randint(1, 3)
            body = []
            for _ in range(body_len):
                if i > 0 and rng.random() < 0.4:
                    body.append(f"INV {rng.choice(names[:i])}")  # only call EARLIER functions -> acyclic
                else:
                    body.append(f"{rng.choice(['ADD', 'MUL'])} {rng.randint(-5, 5)}")
            funcs_src += [f"FUN {name}"] + body + ["END"]
        top = [f"INV {rng.choice(names)}" for _ in range(rng.randint(1, 4))]
        prog = funcs_src + top
        # cross-check against the same evaluator strategy but computed via SnowCal-with-REPEAT
        # in the mod-arithmetic Part3 engine (REPEAT 1 name === INV name), applied at Python-int
        # scale small enough that mod never actually triggers.
        expected = impl.run_snowcal(prog)
        top_mod = [line.replace("INV ", "REPEAT 1 ") for line in top]
        actual_mod = impl.run_snowcal_mod(funcs_src + top_mod)
        assert actual_mod == expected % MOD, prog


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_repeat_worked_example(impl):
    prog = ["ADD 3", "FUN double", "MUL 2", "END", "REPEAT 5 double"]
    assert impl.run_snowcal_mod(prog) == 96


@pytest.mark.part3
@pytest.mark.edge
def test_repeat_zero_times_is_identity(impl):
    prog = ["ADD 3", "FUN double", "MUL 2", "END", "REPEAT 0 double"]
    assert impl.run_snowcal_mod(prog) == 3


@pytest.mark.part3
@pytest.mark.edge
def test_repeat_pure_add_uses_the_a_equals_one_branch(impl):
    # MUL by 1 keeps a == 1 mod MOD, so REPEAT must use the linear (b*k) shortcut, not the
    # geometric-series formula (which would divide by zero: a - 1 == 0).
    prog = ["FUN inc", "ADD 7", "END", "REPEAT 1000 inc"]
    assert impl.run_snowcal_mod(prog) == 7000 % MOD


@pytest.mark.part3
@pytest.mark.edge
def test_repeat_huge_count_matches_modular_formula(impl):
    prog = ["FUN inc", "ADD 1", "END", "REPEAT 1000000000000 inc"]
    assert impl.run_snowcal_mod(prog) == pow(10, 12, MOD)


@pytest.mark.part3
@pytest.mark.edge
def test_repeat_undefined_and_cycle_still_detected(impl):
    with pytest.raises(ValueError):
        impl.run_snowcal_mod(["REPEAT 5 nope"])
    with pytest.raises(ValueError):
        impl.run_snowcal_mod(["FUN loop", "INV loop", "END", "REPEAT 3 loop"])


@pytest.mark.part3
@pytest.mark.edge
def test_repeat_against_brute_force_small_counts(impl):
    rng = random.Random(2)
    for _ in range(150):
        n = rng.randint(1, 20)
        count = rng.randint(0, 40)
        prog = ["FUN f", f"ADD {rng.randint(-9, 9)}", f"MUL {rng.randint(-4, 4)}", "END",
                f"ADD {n}", f"REPEAT {count} f"]
        assert impl.run_snowcal_mod(prog) == _brute_snowcal_mod(prog), (prog, count)


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part3
@pytest.mark.perf
def test_perf_astronomical_repeat_count(run_script):
    prog = ["PART 3", "5", "FUN f", "ADD 1", "MUL 3", "END", "REPEAT 999999999999999 f"]
    r = run_script("\n".join(prog) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nADD 6;SUB 3;MULT 4;DIV 2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "6\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n5\nADD 3\nFUN double\nMUL 2\nEND\nINV double\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "6\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\n5\nADD 3\nFUN double\nMUL 2\nEND\nREPEAT 5 double\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "96\n"
