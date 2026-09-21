import random

import pytest


def _to_base(v: int, base: int) -> str:
    if v == 0:
        return "0"
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = []
    neg = v < 0
    v = abs(v)
    while v:
        v, r = divmod(v, base)
        out.append(digits[r])
    return ("-" if neg else "") + "".join(reversed(out))


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize(
    "a,b,expected",
    [("123", "456", "579"), ("007", "013", "20"), ("999", "1", "1000"), ("0", "0", "0")],
)
def test_part1_worked_examples(impl, a, b, expected):
    assert impl.add_unsigned(a, b) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_part1_single_and_duplicate_lines(impl):
    assert impl.part1(["5 3"]) == ["8"]
    assert impl.part1(["5 3", "5 3"]) == ["8", "8"]


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize("a,b", [("", "5"), ("5", "")])
def test_part1_empty_operand_raises(impl, a, b):
    with pytest.raises(ValueError):
        impl.add_unsigned(a, b)


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize("a,b", [("12a", "3"), ("1 2", "3"), ("-5", "3")])
def test_part1_non_digit_raises(impl, a, b):
    with pytest.raises(ValueError):
        impl.add_unsigned(a, b)


@pytest.mark.part1
@pytest.mark.edge
def test_part1_matches_int_random(impl):
    rng = random.Random(0)
    for _ in range(2000):
        a = str(rng.randint(0, 10**15))
        b = str(rng.randint(0, 10**15))
        assert impl.add_unsigned(a, b) == str(int(a) + int(b)), (a, b)


@pytest.mark.part1
@pytest.mark.io
def test_part1_io(run_script):
    r = run_script("PART 1\n123 456\n007 013\n999 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "579\n20\n1000\n"
    r_empty = run_script("PART 1\n")
    assert r_empty.returncode == 0, r_empty.stderr
    assert r_empty.stdout == ""


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("add_signed", "-5", "3", "-2"),
        ("add_signed", "-0", "0", "0"),
        ("subtract_signed", "5", "8", "-3"),
        ("subtract_signed", "-5", "-8", "3"),
    ],
)
def test_part2_worked_examples(impl, op, a, b, expected):
    assert getattr(impl, op)(a, b) == expected


@pytest.mark.part2
@pytest.mark.fmt
def test_part2_negative_zero_normalizes(impl):
    # "-0" and any result whose magnitude is 0 must print as "0", never "-0"
    assert impl.add_signed("-0", "0") == "0"
    assert impl.add_signed("5", "-5") == "0"
    assert impl.subtract_signed("5", "5") == "0"
    assert not impl.add_signed("5", "-5").startswith("-")


@pytest.mark.part2
@pytest.mark.edge
@pytest.mark.parametrize("a,b", [("-", "3"), ("", "3"), ("+", "3")])
def test_part2_empty_or_bare_sign_raises(impl, a, b):
    with pytest.raises(ValueError):
        impl.add_signed(a, b)


@pytest.mark.part2
@pytest.mark.edge
def test_part2_matches_int_random(impl):
    rng = random.Random(1)
    for _ in range(2000):
        sa = ("-" if rng.random() < 0.5 else "") + str(rng.randint(0, 10**9))
        sb = ("-" if rng.random() < 0.5 else "") + str(rng.randint(0, 10**9))
        assert impl.add_signed(sa, sb) == str(int(sa) + int(sb)), (sa, sb)
        assert impl.subtract_signed(sa, sb) == str(int(sa) - int(sb)), (sa, sb)


@pytest.mark.part2
@pytest.mark.io
def test_part2_io(run_script):
    r = run_script("PART 2\nADD -5 3\nSUB 5 8\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "-2\n-3\n"


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
@pytest.mark.parametrize(
    "a,b,base,expected",
    [
        ("123", "456", 10, "56088"),
        ("-12", "11", 10, "-132"),
        ("ff", "2", 16, "1fe"),
        ("0", "999", 10, "0"),
    ],
)
def test_part3_worked_examples(impl, a, b, base, expected):
    assert impl.multiply_signed(a, b, base) == expected


@pytest.mark.part3
@pytest.mark.edge
def test_part3_zero_operand_short_circuits(impl):
    assert impl.multiply_signed("0", "-999") == "0"
    assert impl.multiply_signed("-7", "0") == "0"


@pytest.mark.part3
@pytest.mark.edge
@pytest.mark.parametrize("base", [0, 1, 37, -5])
def test_part3_invalid_base_raises(impl, base):
    with pytest.raises(ValueError):
        impl.multiply_signed("5", "2", base)


@pytest.mark.part3
@pytest.mark.edge
def test_part3_invalid_digit_for_base_raises(impl):
    with pytest.raises(ValueError):
        impl.multiply_signed("19", "2", 8)  # '9' is not a base-8 digit


@pytest.mark.part3
@pytest.mark.edge
def test_part3_matches_int_random_across_bases(impl):
    rng = random.Random(2)
    for _ in range(1500):
        base = rng.randint(2, 36)
        va, vb = rng.randint(-(10**6), 10**6), rng.randint(-(10**6), 10**6)
        sa, sb = _to_base(va, base), _to_base(vb, base)
        assert impl.multiply_signed(sa, sb, base) == _to_base(va * vb, base), (sa, sb, base)


@pytest.mark.part3
@pytest.mark.perf
def test_part3_perf_large_multiply(impl):
    # two 2000-digit decimal numbers: O(n*m) = 4e6 digit-multiplications, well under 2s in CPython
    rng = random.Random(0)
    a = "".join(rng.choice("0123456789") for _ in range(2000))
    b = "".join(rng.choice("0123456789") for _ in range(2000))
    import time

    t0 = time.perf_counter()
    result = impl.multiply_signed(a, b)
    elapsed = time.perf_counter() - t0
    assert result == str(int(a) * int(b))
    assert elapsed < 2.0, f"took {elapsed:.2f}s"


@pytest.mark.part3
@pytest.mark.io
def test_part3_io(run_script):
    r = run_script("PART 3\n123 456 10\n-12 11 10\nff 2 16\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "56088\n-132\n1fe\n"
