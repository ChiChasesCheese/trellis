import random

import pytest

HEADER = "business_name,business_profile_name,full_statement_descriptor,short_statement_descriptor,url,product_description"
EX1 = [HEADER,
       "Acme Inc,Acme,ACME INC STORE,ACME,https://acme.com,Widgets",
       "Bolt,Bolt Shop,,BOLT,https://bolt.io,Chargers",
       "Cafe Rio,Cafe Rio,CAFE,CAFE,https://caferio.com,Coffee",
       "Dot LLC,Dot,online store,DOT,https://dot.co,Things",
       '"Ed, Inc","Ed",ED INC PAYMENTS,ED INC,https://ed.com,"Books, toys"']
EX1_OUT = ["VERIFIED: Acme Inc", "NOT VERIFIED: Bolt", "NOT VERIFIED: Cafe Rio", "NOT VERIFIED: Dot LLC",
           "VERIFIED: Ed, Inc"]
EX2 = ["Acme Inc,Acme,ACME INC STORE,ACME,https://acme.com,Widgets",
       "Zed,Zed,ZED STORE,STORE,zed.com,Stuff",
       "Foo,Bar,BAZ SERVICES,BAZ,https://baz.io,Svc",
       ",,SHOP,S,https://x,"]
EX2_OUT = ["VERIFIED: Acme Inc", "NOT VERIFIED: Zed (SHORT_DESCRIPTOR, INVALID_URL)",
           "NOT VERIFIED: Foo (NAME_MISMATCH)",
           "NOT VERIFIED:  (EMPTY_FIELD, DESCRIPTOR_LENGTH, DESCRIPTOR_BLACKLISTED, SHORT_DESCRIPTOR, NAME_MISMATCH, INVALID_URL)"]
GOOD = "Acme Inc,Acme,ACME INC STORE,ACME,https://acme.com,Widgets"


def row(full="ACME INC STORE", short="ACME", name="Acme Inc", profile="Acme", url="https://acme.com", product="Widgets"):
    return f"{name},{profile},{full},{short},{url},{product}"


def codes(impl, line, part=5):
    return impl.check_row([f.strip() for f in line.split(",")], part)


# ---------------------------------------------------------------- Part 1: completeness
@pytest.mark.part1
def test_example_3_part1_only(impl):
    rows = ["Dot LLC,Dot,online store,DOT,https://dot.co,Things", "Dot LLC,Dot,online store,DOT,,Things"]
    assert impl.verify(rows, part=1) == ["VERIFIED: Dot LLC", "NOT VERIFIED: Dot LLC"]


@pytest.mark.part1
@pytest.mark.edge
def test_whitespace_only_field_is_empty_and_values_trimmed(impl):
    assert impl.verify([row(product="   ")], part=1) == ["NOT VERIFIED: Acme Inc"]
    assert impl.verify(["  Acme Inc , Acme , ACME INC STORE , ACME , https://acme.com , Widgets "], part=1) == ["VERIFIED: Acme Inc"]


@pytest.mark.part1
@pytest.mark.edge
def test_short_rows_header_and_blank_lines(impl):
    assert impl.verify(["Acme,Acme,ACME INC,ACME"], part=1) == ["NOT VERIFIED: Acme"]  # missing columns = empty
    assert impl.verify([HEADER, "", GOOD, "   "], part=1) == ["VERIFIED: Acme Inc"]
    assert impl.verify([], part=1) == []
    assert impl.verify([HEADER], part=1) == []
    assert impl.verify([GOOD + ",extra,cols"], part=1) == ["VERIFIED: Acme Inc"]  # extra columns ignored


@pytest.mark.part1
@pytest.mark.edge
def test_csv_quoting(impl):
    assert impl.verify(['"Ed, Inc","Ed",ED INC PAYMENTS,ED INC,https://ed.com,"Books, toys"']) == ["VERIFIED: Ed, Inc"]
    assert impl.verify(['"Say ""hi""",Hi,SAY HI SHOP,SAY,https://hi.io,"a ""quoted"" thing"']) == ['VERIFIED: Say "hi"']


# ---------------------------------------------------------------- Part 2: length
@pytest.mark.part2
def test_example_1_parts_1_to_3(impl):
    assert impl.verify(EX1, part=3) == EX1_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_full_descriptor_length_boundaries(impl):
    assert codes(impl, row(full="ACME", short="ACME"), 2) == ["DESCRIPTOR_LENGTH"]          # 4: one below
    assert codes(impl, row(full="ACMEE", short="ACMEE"), 2) == []                            # 5: boundary
    assert codes(impl, row(full="ACME " + "X" * 26, short="ACME"), 2) == []                  # 31: boundary
    assert codes(impl, row(full="ACME " + "X" * 27, short="ACME"), 2) == ["DESCRIPTOR_LENGTH"]  # 32: one above
    assert codes(impl, row(full="", short="ACME"), 2) == ["EMPTY_FIELD", "DESCRIPTOR_LENGTH"]


@pytest.mark.part2
@pytest.mark.edge
def test_length_counted_after_trim_and_part_gating(impl):
    assert impl.verify(["Acme,Acme,   ACME   ,ACME,https://acme.com,W"], part=2) == ["NOT VERIFIED: Acme"]
    assert impl.verify(["Acme,Acme,   ACME   ,ACME,https://acme.com,W"], part=1) == ["VERIFIED: Acme"]


# ---------------------------------------------------------------- Part 3: blacklist
@pytest.mark.part3
@pytest.mark.edge
def test_blacklist_case_whitespace_whole_string(impl):
    for bad in ["ONLINE STORE", "online store", " Shop ", "General   Merchandise", "retail", "eCommerce"]:
        assert "DESCRIPTOR_BLACKLISTED" in codes(impl, row(full=bad, short=bad.split()[0]), 3), bad  # (SHOP is also < 5)
    assert codes(impl, row(full="SHOP ACME", short="SHOP"), 3) == []
    assert codes(impl, row(full="RETAILER", short="RETAILER"), 3) == []


@pytest.mark.part3
@pytest.mark.edge
def test_blacklisted_verified_under_part2(impl):
    r = "Dot LLC,Dot,online store,DOT,https://dot.co,Things"
    assert impl.verify([r], part=2) == ["VERIFIED: Dot LLC"]
    assert impl.verify([r], part=3) == ["NOT VERIFIED: Dot LLC"]


# ---------------------------------------------------------------- Part 4: short descriptor + names
@pytest.mark.part4
@pytest.mark.edge
def test_short_descriptor_length_and_first_word(impl):
    assert codes(impl, row(short="A"), 4) == ["SHORT_DESCRIPTOR"]            # 1: one below
    assert codes(impl, row(short="AC"), 4) == ["SHORT_DESCRIPTOR"]           # 2 chars but first word 'ac' != 'acme'
    assert codes(impl, row(short="ACME"), 4) == []
    assert codes(impl, row(short="ACME INC S"), 4) == []                     # 10: boundary
    assert codes(impl, row(short="ACME INC ST"), 4) == ["SHORT_DESCRIPTOR"]  # 11: one above
    assert codes(impl, row(short="acme"), 4) == []                           # first word case-insensitive
    assert codes(impl, row(short="STORE"), 4) == ["SHORT_DESCRIPTOR"]


@pytest.mark.part4
@pytest.mark.edge
def test_name_mismatch_business_or_profile(impl):
    assert codes(impl, row(name="Foo", profile="Bar", full="BAZ SERVICES", short="BAZ"), 4) == ["NAME_MISMATCH"]
    assert codes(impl, row(name="Foo", profile="Baz", full="BAZ SERVICES", short="BAZ"), 4) == []   # profile matches
    assert codes(impl, row(name="services", profile="Bar", full="BAZ SERVICES", short="BAZ"), 4) == []  # case-insensitive
    assert codes(impl, row(name="", profile="", full="BAZ SERVICES", short="BAZ"), 4) == ["EMPTY_FIELD", "NAME_MISMATCH"]


# ---------------------------------------------------------------- Part 5: url
@pytest.mark.part5
def test_example_2_all_parts_with_reasons(impl):
    assert impl.verify(EX2, part=5, reasons=True) == EX2_OUT
    assert impl.verify(EX2, part=5) == ["VERIFIED: Acme Inc", "NOT VERIFIED: Zed", "NOT VERIFIED: Foo", "NOT VERIFIED: "]


@pytest.mark.part5
@pytest.mark.edge
def test_url_rules(impl):
    ok = ["https://acme.com", "http://acme.com", "HTTP://shop.acme.io/path?x=1", "https://acme.com:8443/x", "https://a.b.c#frag"]
    bad = ["acme.com", "ftp://acme.com", "https://localhost", "https://.com", "https://acme.", "https://", "https:/acme.com",
           "https://acme com", "www.acme.com"]
    for u in ok:
        assert impl.valid_url(u), u
        assert codes(impl, row(url=u), 5) == [], u
    for u in bad:
        assert not impl.valid_url(u), u
        assert codes(impl, row(url=u), 5) == ["INVALID_URL"], u
    assert codes(impl, row(url="acme.com"), 4) == []  # rule 5 not applied under PART 4


@pytest.mark.part5
@pytest.mark.fmt
def test_reason_codes_fixed_order_and_once(impl):
    r = "X,Y,RETAIL,Z,nope,P"  # blacklist + length ok(6) + short first word + name + url
    assert impl.verify([r], reasons=True) == ["NOT VERIFIED: X (DESCRIPTOR_BLACKLISTED, SHORT_DESCRIPTOR, NAME_MISMATCH, INVALID_URL)"]
    assert impl.check_row(["", "", "", "", "", ""]) == ["EMPTY_FIELD", "DESCRIPTOR_LENGTH", "SHORT_DESCRIPTOR", "NAME_MISMATCH", "INVALID_URL"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 3\n" + "\n".join(EX1) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX1_OUT) + "\n"


@pytest.mark.part5
@pytest.mark.io
def test_stdin_reasons_default_part_and_empty(run_script):
    r = run_script("PART 5 REASONS\n" + "\n".join(EX2) + "\n")
    assert r.stdout == "\n".join(EX2_OUT) + "\n"
    assert run_script("\n".join(EX2) + "\n").stdout == "VERIFIED: Acme Inc\nNOT VERIFIED: Zed\nNOT VERIFIED: Foo\nNOT VERIFIED: \n"
    assert run_script("").stdout == ""


@pytest.mark.part5
@pytest.mark.perf
def test_perf_100k_rows(run_script):
    rng = random.Random(0)
    fulls = ["ACME INC STORE", "online store", "ACME", "BAZ SERVICES", "\"Ed, Inc\" PAYMENTS"]
    lines = [HEADER]
    for i in range(100_000):
        full = rng.choice(fulls)
        lines.append(f'"Acme Inc {i}",Acme,{full.replace(chr(34), "")},{rng.choice(["ACME", "STORE", "A"])},'
                     f'{rng.choice(["https://acme.com", "acme.com", "https://x"])},"Widgets, gadgets"')
    r = run_script("PART 5 REASONS\n" + "\n".join(lines) + "\n", timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 100_000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
