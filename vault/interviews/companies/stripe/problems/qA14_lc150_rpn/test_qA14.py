"""qA14 LC 150 Evaluate Reverse Polish Notation — tests.

RECONSTRUCTED TRAINING PROBLEM (title-only mirror entry) -- see problem.md's warning block.
Part 1's LC examples are LeetCode's own published examples; everything else was produced by
running solution.py.
"""

import random

import pytest


def _floor_div(a, b):
    """What // would give -- used to build cases where floor and truncation disagree."""
    return a // b


def _truncate_div(a, b):
    """Independent (test-side) truncate-toward-zero division, used as an oracle."""
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def _gen_valid_rpn(rng, n_leaves):
    """Build a random, always-valid RPN token list plus its correct value, by repeatedly
    combining two random pending sub-expressions with a random operator (falling back off '/'
    when the divisor would be zero). Independent of the implementation under test."""
    nodes = [([str(v)], v) for v in (rng.randint(-20, 20) for _ in range(n_leaves))]
    while len(nodes) > 1:
        a_tokens, a_val = nodes.pop(rng.randrange(len(nodes)))
        b_tokens, b_val = nodes.pop(rng.randrange(len(nodes)))
        op = rng.choice("+-*/")
        if op == "/" and b_val == 0:
            op = "+"
        if op == "+":
            val = a_val + b_val
        elif op == "-":
            val = a_val - b_val
        elif op == "*":
            val = a_val * b_val
        else:
            val = _truncate_div(a_val, b_val)
        nodes.append((a_tokens + b_tokens + [op], val))
    return nodes[0]


# ---------------------------------------------------------------- Part 1: LC 150 evaluate
@pytest.mark.part1
def test_lc_examples(impl):
    assert impl.evaluate_rpn(["2", "1", "+", "3", "*"]) == 9
    assert impl.evaluate_rpn(["4", "13", "5", "/", "+"]) == 6
    assert impl.evaluate_rpn(
        ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
    ) == 22


@pytest.mark.part1
def test_single_operand(impl):
    assert impl.evaluate_rpn(["5"]) == 5
    assert impl.evaluate_rpn(["-3"]) == -3
    assert impl.evaluate_rpn(["0"]) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_division_truncates_toward_zero_not_floor(impl):
    # -7/2 = -3.5: truncation gives -3, floor (//) gives -4 -- these must disagree here
    assert impl.evaluate_rpn(["-7", "2", "/"]) == -3
    assert _floor_div(-7, 2) == -4
    assert impl.evaluate_rpn(["7", "-2", "/"]) == -3
    assert impl.evaluate_rpn(["-7", "-2", "/"]) == 3
    assert impl.evaluate_rpn(["6", "3", "/"]) == 2  # exact multiple: doesn't distinguish the rule


@pytest.mark.part1
@pytest.mark.edge
def test_negative_operands_and_multidigit(impl):
    assert impl.evaluate_rpn(["-13", "5", "+"]) == -8
    assert impl.evaluate_rpn(["100", "-1", "*"]) == -100
    assert impl.evaluate_rpn(["-3", "-4", "+"]) == -7


@pytest.mark.part1
def test_subtraction_and_operand_order(impl):
    # order matters: pop b first, then a; a - b, not b - a
    assert impl.evaluate_rpn(["10", "3", "-"]) == 7
    assert impl.evaluate_rpn(["3", "10", "-"]) == -7


@pytest.mark.part1
def test_matches_independent_oracle_on_random_valid_expressions(impl):
    rng = random.Random(0)
    for _ in range(500):
        tokens, expected = _gen_valid_rpn(rng, rng.randint(1, 6))
        assert impl.evaluate_rpn(tokens) == expected, tokens


# ---------------------------------------------------------------- Part 2: trace
@pytest.mark.part2
def test_trace_example(impl):
    assert impl.evaluate_rpn_trace(["2", "1", "+", "3", "*"]) == [
        "2 + 1 = 3",
        "3 * 3 = 9",
        "RESULT 9",
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_trace_zero_operators(impl):
    assert impl.evaluate_rpn_trace(["5"]) == ["RESULT 5"]
    assert impl.evaluate_rpn_trace(["-3"]) == ["RESULT -3"]


@pytest.mark.part2
def test_trace_second_lc_example(impl):
    assert impl.evaluate_rpn_trace(["4", "13", "5", "/", "+"]) == [
        "13 / 5 = 2",
        "4 + 2 = 6",
        "RESULT 6",
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_trace_shows_original_operands_not_rederived(impl):
    lines = impl.evaluate_rpn_trace(["-7", "2", "/"])
    assert lines == ["-7 / 2 = -3", "RESULT -3"]


@pytest.mark.part2
@pytest.mark.fmt
def test_trace_line_format_exact(impl):
    lines = impl.evaluate_rpn_trace(["10", "3", "-"])
    assert lines[0] == "10 - 3 = 7"
    assert all(isinstance(x, str) for x in lines)


# ---------------------------------------------------------------- Part 3: safe / error handling
@pytest.mark.part3
def test_safe_success_cases(impl):
    assert impl.evaluate_rpn_safe(["3", "4", "+"]) == "7"
    assert impl.evaluate_rpn_safe(["-7", "2", "/"]) == "-3"
    assert impl.evaluate_rpn_safe(["5"]) == "5"


@pytest.mark.part3
@pytest.mark.edge
def test_safe_empty_input(impl):
    assert impl.evaluate_rpn_safe([]) == "ERROR empty_input"


@pytest.mark.part3
@pytest.mark.edge
def test_safe_unknown_token(impl):
    assert impl.evaluate_rpn_safe(["1", "^", "2"]) == "ERROR unknown_token"
    assert impl.evaluate_rpn_safe(["3.5", "+"]) == "ERROR unknown_token"
    assert impl.evaluate_rpn_safe(["+3"]) == "ERROR unknown_token"


@pytest.mark.part3
@pytest.mark.edge
def test_safe_insufficient_operands(impl):
    assert impl.evaluate_rpn_safe(["+"]) == "ERROR insufficient_operands"
    assert impl.evaluate_rpn_safe(["5", "+"]) == "ERROR insufficient_operands"


@pytest.mark.part3
@pytest.mark.edge
def test_safe_division_by_zero(impl):
    assert impl.evaluate_rpn_safe(["1", "0", "/"]) == "ERROR division_by_zero"
    assert impl.evaluate_rpn_safe(["0", "0", "/"]) == "ERROR division_by_zero"


@pytest.mark.part3
@pytest.mark.edge
def test_safe_trailing_operands(impl):
    assert impl.evaluate_rpn_safe(["1", "2"]) == "ERROR trailing_operands"
    assert impl.evaluate_rpn_safe(["1", "2", "3", "+"]) == "ERROR trailing_operands"


@pytest.mark.part3
@pytest.mark.edge
def test_safe_priority_order_leftmost_error_wins(impl):
    # insufficient_operands at token 0 fires before the leftover "0" could ever be flagged
    assert impl.evaluate_rpn_safe(["/", "0"]) == "ERROR insufficient_operands"
    # division_by_zero at token index 2 fires before the later "9","9" trailing pair is reached
    assert impl.evaluate_rpn_safe(["1", "0", "/", "9", "9"]) == "ERROR division_by_zero"


@pytest.mark.part3
@pytest.mark.fmt
def test_safe_never_raises_on_garbage(impl):
    garbage_inputs = [[], ["/"], ["*", "*", "*"], ["--5"], ["5", "5", "5", "5"], ["abc", "+"]]
    for tokens in garbage_inputs:
        result = impl.evaluate_rpn_safe(tokens)
        assert isinstance(result, str)
        assert result == result.split("\n")[0]  # single line, no embedded newline


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n2 1 + 3 *\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "9\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n2 1 + 3 *\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2 + 1 = 3\n3 * 3 = 9\nRESULT 9\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\n1 0 /\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "ERROR division_by_zero\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_1e4_tokens(run_script):
    # LC constraint: len(tokens) <= 10^4. Build a long valid left-leaning expression:
    # "5 3 + 3 + 3 + ..." stays a single running total the whole way, O(n).
    rng = random.Random(0)
    n_operands = 5000  # 5000 operands + 4999 '+' operators == 9999 tokens, within 10^4
    tokens = [str(rng.randint(-100, 100))]
    for _ in range(n_operands - 1):
        tokens.append(str(rng.randint(-100, 100)))
        tokens.append("+")
    assert len(tokens) <= 10_000
    r = run_script("PART 1\n" + " ".join(tokens) + "\n", timeout=10)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
