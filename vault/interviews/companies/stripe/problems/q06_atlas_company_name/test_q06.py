import random

import pytest

AV, NA = "Name Available", "Name Not Available"

EX1 = ["REGISTERED", "Llama, Inc.", "Acme & Sons Corp.", "REQUESTS",
       "1|The Llama", "2|acme and sons", "3|Llama Friends", "4|Llama Friends", "5|The Inc."]
EX1_OUT = [f"1|{NA}", f"2|{NA}", f"3|{AV}", f"4|{AV}", f"5|{NA}"]

EX2 = ["1|Llama, Inc.", "2|The Llama", "3|Llama And Friend, Inc.", "4|And Llama Friend, Inc.",
       "5|Llama,  Inc.", "6| &Co, LLC.", "1|LLAMA"]
EX2_OUT = [f"1|{AV}", f"2|{NA}", f"3|{AV}", f"4|{AV}", f"5|{NA}", f"6|{AV}", f"1|{NA}"]

EX3 = ["1|Llama, Inc.", "2|The Llama", "3|Llama And Friend, Inc.", "4|And Llama Friend, Inc.",
       "5|Llama,  Inc.", "6| &Co, LLC.", "RECLAIM,1,Llama, Inc.", "7|Llama", "8|Co", "9|and co",
       "RECLAIM,6, &Co, LLC.", "10|Co"]
EX3_OUT = [f"1|{AV}", f"2|{NA}", f"3|{AV}", f"4|{AV}", f"5|{NA}", f"6|{AV}", f"7|{AV}", f"8|{NA}", f"9|{AV}", f"10|{AV}"]

EX4 = ["1|Acme", "RECLAIM,2,Acme", "2|ACME", "RECLAIM,1,acme inc", "2|Acme"]
EX4_OUT = [f"1|{AV}", f"2|{NA}", f"2|{AV}"]


# ---------------------------------------------------------------- Part 1: normalization + stateless check
@pytest.mark.part1
def test_example1_stateless(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.parametrize("raw,want", [
    ("The Llama, Inc.", "llama"), ("Llama And Friend, Inc.", "llama friend"), ("And Llama Friend, Inc.", "and llama friend"),
    (" &Co, LLC.", "co"), ("LLAMA", "llama"), ("Llama,  Inc.", "llama"), ("Llama Inc. LLC Corp.", "llama"),
    ("Acme L.L.C.", "acme"), ("Inc Llama", "inc llama"), ("The And Co", "and co"), ("An  Apple", "apple"),
    ("A", ""), ("Inc.", ""), ("&,", ""), ("", ""), ("The Inc.", ""), ("x  b\tc", "x b c"),
])
def test_normalize_cases(impl, raw, want):
    assert impl.normalize(raw) == want


@pytest.mark.part1
@pytest.mark.edge
def test_normalize_other_punctuation_flag(impl):
    assert impl.normalize("Foo-Bar's") == "foo bar s"
    assert impl.normalize("Foo-Bar's", strip_punctuation=False) == "foo-bar's"


@pytest.mark.part1
@pytest.mark.edge
def test_part1_empty_name_never_available_and_no_registry(impl):
    lines = ["REGISTERED", "REQUESTS", "1|Inc.", "2|The", "3|,", "4|X", "5|x"]
    assert impl.part1(lines) == [f"1|{NA}", f"2|{NA}", f"3|{NA}", f"4|{AV}", f"5|{AV}"]
    assert impl.part1(["REGISTERED", "Zed", "REQUESTS"]) == []
    assert impl.part1([]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_part1_persist_flag_matches_repo_wording(impl):
    assert impl.part1(["1|Zed", "2|zed"], persist=True) == [f"1|{AV}", f"2|{NA}"]
    assert impl.part1(["1|Zed", "2|zed"]) == [f"1|{AV}", f"2|{AV}"]


@pytest.mark.part1
@pytest.mark.fmt
def test_output_format_and_account_whitespace(impl):
    assert impl.part1(["REGISTERED", "  The Llama Corp  ", "REQUESTS", " 42 |  llama  "]) == ["42|Name Not Available"]


# ---------------------------------------------------------------- Part 2: persistent registry
@pytest.mark.part2
def test_example2_persistent(impl):
    assert impl.part2(EX2) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_rejected_request_registers_nothing_and_same_account_blocked(impl):
    assert impl.part2(["1|Inc.", "2|Zed", "2|Zed", "3|The Zed, LLC"]) == [f"1|{NA}", f"2|{AV}", f"2|{NA}", f"3|{NA}"]


@pytest.mark.part2
@pytest.mark.edge
def test_registered_block_plus_registry(impl):
    lines = ["REGISTERED", "Acme", "REQUESTS", "1|acme corp.", "1|Beta", "2|The beta, inc."]
    assert impl.part2(lines) == [f"1|{NA}", f"1|{AV}", f"2|{NA}"]


@pytest.mark.part2
@pytest.mark.edge
def test_leading_and_is_distinct_but_inner_and_is_not(impl):
    assert impl.part2(["1|Salt And Pepper", "2|Salt Pepper", "3|And Salt Pepper", "4|and salt pepper"]) == \
        [f"1|{AV}", f"2|{NA}", f"3|{AV}", f"4|{NA}"]


@pytest.mark.part2
@pytest.mark.edge
def test_reclaim_lines_ignored_in_part2(impl):
    assert impl.part2(["1|Zed", "RECLAIM,1,Zed", "2|Zed"]) == [f"1|{AV}", f"2|{NA}"]


# ---------------------------------------------------------------- Part 3: reclaim
@pytest.mark.part3
def test_example3_verbatim_sample(impl):
    assert impl.part3(EX3) == EX3_OUT


@pytest.mark.part3
def test_example4_wrong_account_ignored(impl):
    assert impl.part3(EX4) == EX4_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_reclaim_unregistered_block_name_and_twice(impl):
    lines = ["REGISTERED", "Acme", "REQUESTS", "RECLAIM,1,Acme", "1|Acme", "RECLAIM,1,Nope", "1|Nope",
             "RECLAIM,1,Nope", "RECLAIM,1,Nope", "2|nope", "1|nope"]
    assert impl.part3(lines) == [f"1|{NA}", f"1|{AV}", f"2|{AV}", f"1|{NA}"]


@pytest.mark.part3
@pytest.mark.edge
def test_reclaim_matches_normalized_form_and_keeps_others(impl):
    lines = ["1|Llama, Inc.", "1|Llama Friend", "RECLAIM,1,THE LLAMA LLC", "2|llama", "2|llama friend", "1|llama"]
    assert impl.part3(lines) == [f"1|{AV}", f"1|{AV}", f"2|{AV}", f"2|{NA}", f"1|{NA}"]


@pytest.mark.part3
@pytest.mark.edge
def test_reclaim_account_whitespace_and_case_of_keyword(impl):
    assert impl.part3(["7|Zed", "reclaim, 7 ,Zed", "8|zed"]) == [f"7|{AV}", f"8|{AV}"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 3\n" + "\n".join(EX3) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX3_OUT) + "\n"
    r = run_script("PART 1\n" + "\n".join(EX1) + "\n")
    assert r.stdout == "\n".join(EX1_OUT) + "\n"
    r = run_script("\n".join(EX2) + "\n")  # no PART line -> part 3 (superset of part 2 here)
    assert r.stdout == "\n".join(EX2_OUT) + "\n"
    assert run_script("PART 2\n").stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_requests(run_script):
    rng = random.Random(0)
    words = [f"w{i}" for i in range(3000)]
    lines = ["PART 3"]
    for i in range(100_000):
        name = " ".join(rng.choice(words) for _ in range(rng.randint(1, 3))) + rng.choice(["", ", Inc.", " LLC", " & Co"])
        if rng.random() < 0.1:
            lines.append(f"RECLAIM,{rng.randrange(500)},{name}")
        else:
            lines.append(f"{rng.randrange(500)}|The {name}")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == sum(1 for l in lines[1:] if "|" in l)
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
