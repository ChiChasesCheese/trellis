import random

import pytest

EX1 = [
    "API: amount=1000&merchant=121212",
    "API: merchant=121212&amount=-250",
    "BAL: merchant=121212",
    "BAL: merchant=999",
    "API: amount=abc&merchant=1",
    "API: amount=5&amount=7&merchant=1&foo=bar",
    "BAL: merchant=1",
]
EX1_OUT = ["750", "0", "7"]
EX2 = [
    "RULE: amount==100",
    "RULE: merchant != 121212",
    "API: amount=100&merchant=121212",
    "API: amount=50&merchant=777",
    "API: amount=50&merchant=121212",
    "BAL: merchant=121212",
    "BAL: merchant=777",
]
EX2_OUT = ["50", "0"]
EX3 = [
    'RULE: BLOCK if (:card_country: = "US" AND :large_amount:)',
    'RULE: ACCEPT if ("United States" = :country_name:)',
    'RULE: BLOCK if (:currency: != "usd")',
    "TXN: card_country=US&large_amount=true&country_name=United States",
    "TXN: card_country=US&large_amount=false&country_name=United States&currency=eur",
    "TXN: card_country=CA&currency=eur",
    "TXN: card_country=CA",
]
EX3_OUT = ["BLOCK", "ACCEPT", "BLOCK", "ACCEPT"]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_part1(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.fmt
def test_unknown_merchant_zero_and_negative_balance(impl):
    assert impl.part1(["BAL: merchant=x"]) == ["0"]
    assert impl.part1(["API: amount=-5&merchant=x", "BAL: merchant=x", "API: amount=0&merchant=x", "BAL: merchant=x"]) == ["-5", "-5"]


@pytest.mark.part1
@pytest.mark.edge
def test_malformed_lines_ignored(impl):
    lines = [
        "API: merchant=x",             # no amount
        "API: amount=10",              # no merchant
        "API: amount=1.5&merchant=x",  # not an integer
        "API: amount=10&merchant=",    # empty merchant
        "FOO: amount=10&merchant=x",   # unknown prefix
        "garbage line",
        "API amount=10&merchant=x",    # no colon
        "BAL: merchant=x",
    ]
    assert impl.part1(lines) == ["0"]


@pytest.mark.part1
@pytest.mark.edge
def test_key_order_duplicates_unknown_keys_and_spaces(impl):
    lines = ["API:merchant=m&extra=1&amount=3&amount=4", "   API:   amount=6&merchant=m   ", "BAL:merchant=m"]
    assert impl.part1(lines) == ["10"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_and_no_bal(impl):
    assert impl.part1([]) == []
    assert impl.part1(["API: amount=1&merchant=a"]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_big_amounts_stay_exact(impl):
    lines = ["API: amount=999999999999&merchant=a"] * 3 + ["BAL: merchant=a"]
    assert impl.part1(lines) == ["2999999999997"]


@pytest.mark.part1
def test_part1_ignores_rules(impl):
    assert impl.part1(["RULE: amount==1", "API: amount=1&merchant=a", "BAL: merchant=a"]) == ["1"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_part2(impl):
    assert impl.part2(EX2) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_operator_spacing_variants(impl):
    for rule in ["amount==100", "amount == 100", "amount ==100", "amount== 100", "  amount==100  "]:
        assert impl.part2([f"RULE: {rule}", "API: amount=100&merchant=a", "API: amount=101&merchant=a", "BAL: merchant=a"]) == ["101"], rule


@pytest.mark.part2
@pytest.mark.edge
def test_missing_field_never_matches_even_not_equal(impl):
    lines = ["RULE: country != US", "API: amount=5&merchant=a", "API: amount=7&merchant=a&country=CA", "BAL: merchant=a"]
    assert impl.part2(lines) == ["5"]


@pytest.mark.part2
@pytest.mark.edge
def test_rules_apply_only_to_later_lines_and_any_rule_blocks(impl):
    lines = [
        "API: amount=100&merchant=a",   # before the rule: accepted
        "RULE: amount==100",
        "API: amount=100&merchant=a",   # blocked
        "RULE: merchant==b",
        "API: amount=1&merchant=b",     # blocked by second rule
        "API: amount=1&merchant=a",     # accepted
        "BAL: merchant=a", "BAL: merchant=b",
    ]
    assert impl.part2(lines) == ["101", "0"]


@pytest.mark.part2
@pytest.mark.edge
def test_numeric_vs_string_compare_and_negative(impl):
    assert impl.part2(["RULE: amount==0100", "API: amount=100&merchant=a", "BAL: merchant=a"]) == ["0"]
    assert impl.part2(["RULE: amount==-5", "API: amount=-5&merchant=a", "API: amount=5&merchant=a", "BAL: merchant=a"]) == ["5"]
    assert impl.part2(["RULE: merchant==ab", "API: amount=1&merchant=AB", "BAL: merchant=AB"]) == ["1"]  # case-sensitive strings


@pytest.mark.part2
@pytest.mark.edge
def test_numeric_operators_variant(impl):
    lines = ["RULE: amount > 100", "RULE: amount<=0", "API: amount=101&merchant=a", "API: amount=100&merchant=a",
             "API: amount=0&merchant=a", "API: amount=1&merchant=a", "BAL: merchant=a"]
    assert impl.part2(lines) == ["101"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_part3_lines(impl):
    assert impl.part3(EX3) == EX3_OUT


@pytest.mark.part3
def test_example_part3_function(impl):
    f = impl.should_accept_transaction
    assert f({"a": "1"}, ['BLOCK if (:a: = "1" OR :b: = "2")']) is False
    assert f({"a": "1", "b": "x"}, ['BLOCK if (:a: = "1" AND :b: = "2")']) is True
    assert f({}, []) is True


@pytest.mark.part3
@pytest.mark.edge
def test_first_match_wins_and_default_accept(impl):
    f = impl.should_accept_transaction
    rules = ['ACCEPT if (:country: = "US")', 'BLOCK if (:country: = "US")']
    assert f({"country": "US"}, rules) is True
    assert f({"country": "US"}, list(reversed(rules))) is False
    assert f({"country": "CA"}, rules) is True  # no match


@pytest.mark.part3
@pytest.mark.edge
def test_swapped_operands_constants_with_spaces_and_not_equal(impl):
    f = impl.should_accept_transaction
    assert f({"city": "New York"}, ['BLOCK if ("New York" = :city:)']) is False
    assert f({"city": "New York"}, ['BLOCK if (:city: = "New York")']) is False
    assert f({"city": "new york"}, ['BLOCK if (:city: = "New York")']) is True  # case-sensitive
    assert f({"city": "Boston"}, ['BLOCK if (:city: != "New York")']) is False
    assert f({"a": "x", "b": "x"}, ['BLOCK if (:a: = :b:)']) is False  # field vs field
    assert f({"a": "x"}, ['BLOCK if ("x" = "x")']) is False  # const vs const


@pytest.mark.part3
@pytest.mark.edge
def test_missing_field_is_false_even_for_not_equal_and_booleans(impl):
    f = impl.should_accept_transaction
    assert f({}, ['BLOCK if (:country: != "US")']) is True
    assert f({}, ['BLOCK if (:stolen:)']) is True
    assert f({"stolen": "true"}, ['BLOCK if (:stolen:)']) is False
    assert f({"stolen": "TRUE"}, ['BLOCK if (:stolen:)']) is False
    assert f({"stolen": "1"}, ['BLOCK if (:stolen:)']) is True
    assert f({"stolen": "false"}, ['BLOCK if (:stolen:)']) is True


@pytest.mark.part3
@pytest.mark.edge
def test_and_binds_tighter_than_or_and_parentheses(impl):
    f = impl.should_accept_transaction
    txn = {"a": "true", "b": "false", "c": "false"}
    # a OR (b AND c) -> true -> BLOCK
    assert f(txn, ["BLOCK if (:a: OR :b: AND :c:)"]) is False
    # (a OR b) AND c -> false -> no match
    assert f(txn, ["BLOCK if ((:a: OR :b:) AND :c:)"]) is True
    assert f(txn, ["BLOCK if (:c: AND :b: OR :a:)"]) is False
    # no outer parentheses, keywords in any case
    assert f({"known_stolen_card": "true", "large_amount": "true"}, ["block IF :known_stolen_card: and :large_amount:"]) is False
    assert f({"known_stolen_card": "true", "large_amount": "false"}, ["BLOCK if (:known_stolen_card: AND :large_amount:)"]) is True


@pytest.mark.part3
@pytest.mark.edge
def test_malformed_rules(impl):
    f = impl.should_accept_transaction
    for bad in ['BLOCK if (:a: = "1"', 'BLOCK :a: = "1"', 'MAYBE if (:a: = "1")', 'BLOCK if (:a: = )', 'BLOCK if ("x")', "BLOCK if (:a: AND)"]:
        with pytest.raises(ValueError):
            f({"a": "1"}, [bad])
    # the line driver skips malformed rules and keeps going
    assert impl.part3(['RULE: BLOCK if (:a: = "1"', 'RULE: BLOCK if (:a: = "2")', "TXN: a=1", "TXN: a=2"]) == ["ACCEPT", "BLOCK"]


@pytest.mark.part3
def test_part3_driver_keeps_ledger_working(impl):
    lines = ["API: amount=5&merchant=m", 'RULE: BLOCK if (:m: = "1")', "BAL: merchant=m", "TXN: m=1", "TXN: m=2", "TXN: x=y"]
    assert impl.part3(lines) == ["5", "BLOCK", "ACCEPT", "ACCEPT"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 3\n" + "\n".join(EX3) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX3_OUT) + "\n"
    r = run_script("PART 1\n" + "\n".join(EX1) + "\n")
    assert r.stdout == "\n".join(EX1_OUT) + "\n"
    r = run_script("PART 2\n" + "\n".join(EX2) + "\n")
    assert r.stdout == "\n".join(EX2_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("PART 1\n")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_lines_with_rules(run_script):
    rng = random.Random(0)
    lines = [f'RULE: BLOCK if (:country: = "C{i}" AND :amount_big:)' for i in range(20)]
    lines.append('RULE: ACCEPT if (:vip: OR (:country: = "US" AND :amount_big: != "true"))')
    lines += [f"RULE: amount=={i}" for i in range(20)]  # ignored by part 3 (not radar syntax)
    n_txn = 0
    for _ in range(100_000):
        k = rng.random()
        if k < 0.4:
            lines.append(f"API: amount={rng.randrange(-1000, 1000)}&merchant=m{rng.randrange(500)}")
        elif k < 0.5:
            lines.append(f"BAL: merchant=m{rng.randrange(500)}")
        else:
            n_txn += 1
            lines.append(f"TXN: country=C{rng.randrange(40)}&amount_big={rng.choice(['true', 'false'])}&vip={rng.choice(['true', 'false'])}")
    r = run_script("PART 3\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("ACCEPT") + r.stdout.count("BLOCK") == n_txn
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
