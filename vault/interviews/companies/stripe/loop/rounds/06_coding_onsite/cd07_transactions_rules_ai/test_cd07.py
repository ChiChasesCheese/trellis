import random

import pytest

P1_EX = [
    "RULES",
    "ALLOW if country == US",
    "BLOCK if amount == 10000",
    "TRANSACTIONS",
    "t1,500,USD,US,visa,acme",
    "t2,10000,USD,CA,visa,acme",
    "t3,700,USD,FR,visa,acme",
]
P1_OUT = ["t1 ALLOW (rule 1)", "t2 BLOCK (rule 2)", "t3 ALLOW"]

P2_EX = [
    "RULES",
    "BLOCK if amount > 5000",
    "ALLOW if country in [US, CA]",
    "BLOCK if currency != USD",
    "TRANSACTIONS",
    "t1,6000,USD,US,visa,acme",
    "t2,3000,USD,MX,visa,acme",
    "t3,3000,EUR,FR,visa,acme",
    "t4,3000,USD,CA,visa,acme",
]
P2_OUT = ["t1 BLOCK (rule 1)", "t2 ALLOW", "t3 BLOCK (rule 3)", "t4 ALLOW (rule 2)"]

P3_EX = [
    "RULES",
    "BLOCK if country == US and amount > 5000",
    "ALLOW if (country == CA or country == MX) and not currency == EUR",
    "BLOCK if amount >",
    "TRANSACTIONS",
    "t1,6000,USD,US,visa,acme",
    "t2,3000,USD,CA,visa,acme",
    "t3,3000,EUR,CA,visa,acme",
    "t4,100,USD,FR,visa,acme",
]
P3_OUT = [
    "ERROR line 3: expected a field or value",
    "t1 BLOCK (rule 1)",
    "t2 ALLOW (rule 2)",
    "t3 ALLOW",
    "t4 ALLOW",
]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_part1(impl):
    assert impl.part1(P1_EX) == P1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_no_match_defaults_allow_without_suffix(impl):
    lines = ["RULES", "BLOCK if country == US", "TRANSACTIONS", "t1,0,USD,CA,visa,acme"]
    assert impl.part1(lines) == ["t1 ALLOW"]


@pytest.mark.part1
@pytest.mark.edge
def test_first_matching_rule_wins(impl):
    lines = [
        "RULES",
        "ALLOW if country == US",
        "BLOCK if country == US",
        "TRANSACTIONS",
        "t1,0,USD,US,visa,acme",
    ]
    assert impl.part1(lines) == ["t1 ALLOW (rule 1)"]


@pytest.mark.part1
@pytest.mark.edge
def test_equality_is_string_compare_and_case_sensitive(impl):
    lines = ["RULES", "ALLOW if country == US", "TRANSACTIONS", "t1,0,USD,us,visa,acme"]
    assert impl.part1(lines) == ["t1 ALLOW"]  # "us" != "US", no rule matches -> default ALLOW


@pytest.mark.part1
@pytest.mark.edge
def test_empty_rules_and_empty_transactions(impl):
    assert impl.part1(["RULES", "TRANSACTIONS", "t1,0,USD,US,visa,acme"]) == ["t1 ALLOW"]
    assert impl.part1(["RULES", "ALLOW if country == US", "TRANSACTIONS"]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_short_transaction_row_padded_not_crashed(impl):
    # fewer than 6 columns -> missing trailing fields are "" and just don't match
    lines = ["RULES", "BLOCK if merchant == acme", "TRANSACTIONS", "t1,0,USD"]
    assert impl.part1(lines) == ["t1 ALLOW"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_part2(impl):
    assert impl.part2(P2_EX) == P2_OUT


@pytest.mark.part2
@pytest.mark.fmt
def test_operator_whitespace_variants_all_equivalent(impl):
    variants = ["amount>=5000", "amount >=5000", "amount>= 5000", "amount >= 5000"]
    for cond in variants:
        lines = ["RULES", f"BLOCK if {cond}", "TRANSACTIONS", "t1,5000,USD,US,visa,acme"]
        assert impl.part2(lines) == ["t1 BLOCK (rule 1)"], cond


@pytest.mark.part2
@pytest.mark.edge
def test_numeric_equality_ignores_leading_zeros(impl):
    lines = ["RULES", "BLOCK if amount == 0100", "TRANSACTIONS", "t1,100,USD,US,visa,acme"]
    assert impl.part2(lines) == ["t1 BLOCK (rule 1)"]


@pytest.mark.part2
@pytest.mark.edge
def test_in_list_empty_single_and_several_items(impl):
    lines = [
        "RULES",
        "BLOCK if country in [US, CA, MX]",
        "TRANSACTIONS",
        "t1,0,USD,US,visa,acme",
        "t2,0,USD,FR,visa,acme",
        "t3,0,USD,MX,visa,acme",
    ]
    assert impl.part2(lines) == ["t1 BLOCK (rule 1)", "t2 ALLOW", "t3 BLOCK (rule 1)"]
    lines_one = ["RULES", "BLOCK if country in [US]", "TRANSACTIONS", "t1,0,USD,US,visa,acme"]
    assert impl.part2(lines_one) == ["t1 BLOCK (rule 1)"]
    lines_empty = ["RULES", "BLOCK if country in []", "TRANSACTIONS", "t1,0,USD,US,visa,acme"]
    assert impl.part2(lines_empty) == ["t1 ALLOW"]  # empty list matches nothing, not an error


@pytest.mark.part2
@pytest.mark.edge
def test_all_comparison_operators(impl):
    def run(op, amount):
        lines = ["RULES", f"BLOCK if amount {op} 100", "TRANSACTIONS", f"t1,{amount},USD,US,visa,acme"]
        return impl.part2(lines) == ["t1 BLOCK (rule 1)"]

    assert run("!=", 50) and not run("!=", 100)
    assert run(">", 150) and not run(">", 100)
    assert run("<", 50) and not run("<", 100)
    assert run(">=", 100) and not run(">=", 99)
    assert run("<=", 100) and not run("<=", 101)


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_part3(impl):
    assert impl.part3(P3_EX) == P3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_not_binds_tighter_than_and(impl):
    # "not a and b" == "(not a) and b" -- with country US (a true, not a false) rule never fires
    lines = [
        "RULES",
        "BLOCK if not country == US and amount == 0",
        "TRANSACTIONS",
        "t1,0,USD,US,visa,acme",
    ]
    assert impl.part3(lines) == ["t1 ALLOW"]


@pytest.mark.part3
@pytest.mark.edge
def test_and_binds_tighter_than_or(impl):
    # "a or b and c" == "a or (b and c)". a=false, b=true, c=false -> false; a false alone would
    # also be false under the WRONG "(a or b) and c" reading, so pick values that disambiguate:
    # a=false, b=true, c=true -> right reading: false or (true and true) = true
    #                          -> wrong "(a or b) and c" reading also gives true here, so use a=true
    # a=true, b=false, c=false -> right reading: true or (false and false) = true
    #                            -> wrong reading: (true or false) and false = false  <- disambiguates
    lines = [
        "RULES",
        "BLOCK if country == US or country == FR and amount == 999",
        "TRANSACTIONS",
        "t1,0,USD,US,visa,acme",  # a=True(US), b=False(FR), c=False(amount==999) -> should BLOCK
    ]
    assert impl.part3(lines) == ["t1 BLOCK (rule 1)"]


@pytest.mark.part3
@pytest.mark.edge
def test_nested_parens(impl):
    lines = [
        "RULES",
        "BLOCK if (country == US and (amount > 100 or currency == EUR))",
        "TRANSACTIONS",
        "t1,0,EUR,US,visa,acme",
        "t2,0,USD,US,visa,acme",
    ]
    assert impl.part3(lines) == ["t1 BLOCK (rule 1)", "t2 ALLOW"]


@pytest.mark.part3
@pytest.mark.edge
def test_rule_line_numbers_survive_skipped_error_rules(impl):
    lines = [
        "RULES",
        "BLOCK if amount >",  # invalid -> ERROR line 1
        "ALLOW if country == US",  # valid, still line 2
        "TRANSACTIONS",
        "t1,0,USD,US,visa,acme",
    ]
    out = impl.part3(lines)
    assert out[0] == "ERROR line 1: expected a field or value"
    assert out[1] == "t1 ALLOW (rule 2)"


@pytest.mark.part3
@pytest.mark.edge
def test_various_invalid_rules_each_report_one_error(impl):
    lines = [
        "RULES",
        "BLOCK if (country == US",  # unbalanced paren
        "ALLOW if country == US and",  # missing right operand of 'and'
        "BLOCK if and == US",  # keyword used as operand
        "SOMETHING if country == US",  # bad action keyword
        "TRANSACTIONS",
    ]
    out = impl.part3(lines)
    assert [ln.split(":")[0] for ln in out] == [
        "ERROR line 1",
        "ERROR line 2",
        "ERROR line 3",
        "ERROR line 4",
    ]


@pytest.mark.part3
@pytest.mark.edge
def test_field_vs_field_comparison(impl):
    lines = ["RULES", "BLOCK if country == country", "TRANSACTIONS", "t1,0,USD,US,visa,acme"]
    assert impl.part3(lines) == ["t1 BLOCK (rule 1)"]


@pytest.mark.part3
def test_part3_still_supports_part2_grammar(impl):
    lines = ["RULES", "BLOCK if amount >= 100", "TRANSACTIONS", "t1,100,USD,US,visa,acme"]
    assert impl.part3(lines) == ["t1 BLOCK (rule 1)"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    r = run_script("\n".join(["PART 1"] + P1_EX) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P1_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact_part3(run_script):
    r = run_script("\n".join(["PART 3"] + P3_EX) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P3_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_many_rules_many_transactions(run_script):
    rng = random.Random(0)
    countries = ["US", "CA", "MX", "FR", "DE"]
    rules = [
        f"BLOCK if country == {rng.choice(countries)} and amount > {rng.randrange(0, 10000)}"
        for _ in range(2000)
    ]
    txns = [f"t{i},{rng.randrange(0, 20000)},USD,{rng.choice(countries)},visa,acme" for i in range(20000)]
    stdin = "\n".join(["PART 3", "RULES", *rules, "TRANSACTIONS", *txns]) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == len(txns)
    assert r.seconds < 5.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
