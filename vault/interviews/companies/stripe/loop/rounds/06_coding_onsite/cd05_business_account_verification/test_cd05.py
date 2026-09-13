import json
import random

import pytest

DOC_PART1 = {
    "account": {
        "business_name": "Acme Inc",
        "business_profile": {"url": "", "mcc": "5734"},
        "representative": {"email": "rep@acme.com"},
    },
    "rules": [
        {"requires": ["business_name", "business_profile.url", "business_profile.mcc"]},
        {"requires": ["representative.email", "representative.phone"]},
    ],
}
DOC_PART1_OUT = ["business_profile.url", "representative.phone"]

DOC_PART2 = {
    "account": {
        "business_name": "Acme Inc",
        "business_type": "company",
        "representative": {"email": "", "phone": ""},
        "owners": [
            {"first_name": "Alice"},
            {"first_name": ""},
            {"last_name": "Kim"},
        ],
    },
    "rules": [
        {"requires": ["business_name"]},
        {"when": [{"path": "business_type", "equals": "company"}], "requires": ["owners[].first_name"]},
        {"when": [{"path": "business_type", "equals": "individual"}], "requires": ["ssn_last4"]},
        {"one_of": ["representative.email", "representative.phone"]},
    ],
}
DOC_PART2_OUT = [
    "one_of(representative.email|representative.phone)",
    "owners[1].first_name",
    "owners[2].first_name",
]


# ---------------------------------------------------------------- Part 1: requires only
@pytest.mark.part1
def test_example_part1_missing(impl):
    assert impl.part1(DOC_PART1) == DOC_PART1_OUT


@pytest.mark.part1
def test_example_part1_verified(impl):
    doc = json.loads(json.dumps(DOC_PART1))
    doc["account"]["business_profile"]["url"] = "https://acme.example"
    doc["account"]["representative"]["phone"] = "555-0100"
    assert impl.part1(doc) == ["VERIFIED"]


@pytest.mark.part1
def test_part1_nested_dot_path(impl):
    doc = {"account": {"a": {"b": {"c": "x"}}}, "rules": [{"requires": ["a.b.c", "a.b.d"]}]}
    assert impl.part1(doc) == ["a.b.d"]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_missing_top_level_key_entirely(impl):
    doc = {"account": {}, "rules": [{"requires": ["business_name"]}]}
    assert impl.part1(doc) == ["business_name"]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_duplicate_missing_dedup(impl):
    doc = {"account": {}, "rules": [{"requires": ["x"]}, {"requires": ["x"]}]}
    assert impl.part1(doc) == ["x"]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_empty_rules_is_verified(impl):
    assert impl.part1({"account": {"anything": 1}, "rules": []}) == ["VERIFIED"]


@pytest.mark.part1
@pytest.mark.fmt
def test_part1_sort_is_plain_string_order(impl):
    doc = {"account": {}, "rules": [{"requires": ["b", "B", "a10", "a2"]}]}
    assert impl.part1(doc) == ["B", "a10", "a2", "b"]


# ---------------------------------------------------------------- Part 2: when / one_of / wildcard
@pytest.mark.part2
def test_example_part2(impl):
    assert impl.part2(DOC_PART2) == DOC_PART2_OUT


@pytest.mark.part2
def test_part2_when_gate_skips_rule(impl):
    doc = {
        "account": {"business_type": "company"},
        "rules": [{"when": [{"path": "business_type", "equals": "individual"}], "requires": ["ssn_last4"]}],
    }
    assert impl.part2(doc) == ["VERIFIED"]


@pytest.mark.part2
def test_part2_when_present_false_matches_absent_path(impl):
    doc = {
        "account": {},
        "rules": [{"when": [{"path": "dba_name", "present": False}], "requires": ["legal_name"]}],
    }
    assert impl.part2(doc) == ["legal_name"]


@pytest.mark.part2
def test_part2_when_present_true_requires_existing_key(impl):
    doc = {
        "account": {"legal_name": "Acme"},
        "rules": [{"when": [{"path": "legal_name", "present": True}], "requires": ["ein"]}],
    }
    assert impl.part2(doc) == ["ein"]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_when_multiple_conditions_all_must_match(impl):
    doc = {
        "account": {"business_type": "company", "legal_name": "Acme"},
        "rules": [
            {
                "when": [
                    {"path": "business_type", "equals": "company"},
                    {"path": "legal_name", "equals": "Other"},
                ],
                "requires": ["missing_field"],
            }
        ],
    }
    # second condition fails -> whole rule skipped, even though the first one matched
    assert impl.part2(doc) == ["VERIFIED"]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_equals_is_type_sensitive(impl):
    doc = {
        "account": {"flag": True},
        "rules": [{"when": [{"path": "flag", "equals": "true"}], "requires": ["x"]}],
    }
    # "true" (str) != True (bool) -> when does not match -> rule skipped
    assert impl.part2(doc) == ["VERIFIED"]


@pytest.mark.part2
def test_part2_one_of_satisfied_when_any_nonempty(impl):
    doc = {"account": {"a": "", "b": "x"}, "rules": [{"one_of": ["a", "b"]}]}
    assert impl.part2(doc) == ["VERIFIED"]


@pytest.mark.part2
def test_part2_one_of_all_missing(impl):
    doc = {"account": {}, "rules": [{"one_of": ["a", "b", "c"]}]}
    assert impl.part2(doc) == ["one_of(a|b|c)"]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_wildcard_empty_array_is_vacuous(impl):
    doc = {"account": {"owners": []}, "rules": [{"requires": ["owners[].first_name"]}]}
    assert impl.part2(doc) == ["VERIFIED"]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_wildcard_missing_base_falls_back_to_literal_path(impl):
    doc = {"account": {}, "rules": [{"requires": ["owners[].first_name"]}]}
    assert impl.part2(doc) == ["owners[].first_name"]


@pytest.mark.part2
@pytest.mark.fmt
def test_part2_sort_mixes_one_of_and_plain_paths(impl):
    out = impl.part2(DOC_PART2)
    assert out == DOC_PART2_OUT == sorted(DOC_PART2_OUT)


# ---------------------------------------------------------------- io / perf
@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 2\n" + json.dumps(DOC_PART2) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(DOC_PART2_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1_verified(run_script):
    r = run_script("PART 1\n" + json.dumps({"account": {"x": "y"}, "rules": []}) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "VERIFIED\n"


@pytest.mark.part2
@pytest.mark.perf
def test_perf_large_account_and_ruleset(run_script):
    rng = random.Random(0)
    owners = [{"first_name": f"n{i}", "last_name": f"l{i}"} for i in range(3000)]
    knocked_out = sorted(rng.sample(range(3000), 429))
    for i in knocked_out:
        owners[i]["first_name"] = ""
    account = {"business_name": "Acme", "business_type": "company", "owners": owners}
    rules = [{"when": [{"path": "business_type", "equals": "company"}], "requires": ["owners[].first_name"]}]
    rules += [{"requires": ["business_name"]} for _ in range(199)]  # rules <= 200
    doc = {"account": account, "rules": rules}
    r = run_script("PART 2\n" + json.dumps(doc) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
    lines = r.stdout.strip("\n").split("\n")
    assert len(lines) == len(knocked_out)
