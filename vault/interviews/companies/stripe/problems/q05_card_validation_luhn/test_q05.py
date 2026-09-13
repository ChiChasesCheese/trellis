import itertools
import random

import pytest

P4_SAMPLE_OUT = [
    "4432015112830367,VISA", "4523015112830367,VISA", "4531015112830367,VISA", "4532005112830367,VISA",
    "4532010112830367,VISA", "4532015012830367,VISA", "4532015111830367,VISA", "4532015112330367,VISA",
    "4532015112820367,VISA", "4532015112830267,VISA", "4532015112830317,VISA", "4532015112830366,VISA",
    "4532015112839367,VISA", "4532015152830367,VISA", "4532915112830367,VISA", "4572015112830367,VISA",
]

HACKERRANK_SAMPLE = """9
P1 4532015112830366
P1 4242424242424243
P2 5482334509943
P2 4425233430109994
P2 562523343010901
P3 4242424242424*42
P3 3*8282246310005
P3 **2424242424242
P4 4532015112830367?
"""
HACKERRANK_SAMPLE_OUT = ["VISA", "INVALID_CHECKSUM", "UNKNOWN_NETWORK", "INVALID_CHECKSUM", "UNKNOWN_NETWORK",
                         "VISA,1", "AMEX,1", "AMEX,1", *P4_SAMPLE_OUT]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example1(impl):
    assert impl.part1(["4532015112830366", "4242424242424243", "4242424242424242"]) == ["VISA", "INVALID_CHECKSUM", "VISA"]


@pytest.mark.part1
@pytest.mark.edge
def test_stripe_test_cards_luhn(impl):
    assert impl.luhn_ok("4242424242424242") and impl.luhn_ok("5555555555554444") and impl.luhn_ok("378282246310005")
    assert not impl.luhn_ok("4242424242424241")
    assert impl.part1(["4242424242424241"]) == ["INVALID_CHECKSUM"]


@pytest.mark.part1
@pytest.mark.edge
def test_luhn_doubling_over_nine_and_check_digit_neighbours(impl):
    # 4000000000000002: doubled digits are all 0 except the leading 4 -> 8; sum 8 + 2 = 10 -> valid
    assert impl.part1(["4000000000000002"]) == ["VISA"]
    # exactly one check digit per body: the ten candidates for the last digit contain one valid card
    body = "400000000000000"
    assert sum(impl.luhn_ok(body + d) for d in "0123456789") == 1
    assert impl.part1(["4999999999999996", "4999999999999995"]) == ["VISA", "INVALID_CHECKSUM"]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_blank_lines_and_whitespace(impl):
    assert impl.part1([" 4242424242424242 ", "", "4242424242424241"]) == ["VISA", "INVALID_CHECKSUM"]
    assert impl.part1([]) == []


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example2(impl):
    lines = ["5482334509943", "4425233430109994", "562523343010901", "5555555555554444", "378282246310005"]
    assert impl.part2(lines) == ["UNKNOWN_NETWORK", "INVALID_CHECKSUM", "UNKNOWN_NETWORK", "MASTERCARD", "AMEX"]


@pytest.mark.part2
@pytest.mark.edge
def test_shape_checked_before_checksum(impl):
    # Luhn-valid numbers of unsupported shapes are UNKNOWN_NETWORK, not INVALID_CHECKSUM
    assert impl.part2(["2223003122003222", "6011111111111117"]) == ["UNKNOWN_NETWORK", "UNKNOWN_NETWORK"]
    assert impl.part2(["424242424242424", "42424242424242424"]) == ["UNKNOWN_NETWORK", "UNKNOWN_NETWORK"]  # 15 / 17 digits


@pytest.mark.part2
@pytest.mark.edge
def test_mastercard_prefix_boundaries(impl):
    def card(prefix):  # build a Luhn-valid 16-digit number with the given prefix
        body = prefix + "0" * (15 - len(prefix))
        return next(body + d for d in "0123456789" if impl.luhn_ok(body + d))
    assert impl.part2([card("50"), card("51"), card("55"), card("56")]) == ["UNKNOWN_NETWORK", "MASTERCARD", "MASTERCARD", "UNKNOWN_NETWORK"]


@pytest.mark.part2
@pytest.mark.edge
def test_amex_prefix_and_length(impl):
    def card(prefix, length):
        body = prefix + "0" * (length - 1 - len(prefix))
        return next(body + d for d in "0123456789" if impl.luhn_ok(body + d))
    assert impl.part2([card("34", 15), card("37", 15), card("35", 15), card("37", 16), card("4", 15)]) == \
        ["AMEX", "AMEX", "UNKNOWN_NETWORK", "UNKNOWN_NETWORK", "UNKNOWN_NETWORK"]
    assert impl.part2(["378282246310006"]) == ["INVALID_CHECKSUM"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example3(impl):
    assert impl.part3(["4242424242424*42", "3*8282246310005", "**2424242424242", "5*5555555555444*"]) == \
        ["VISA,1", "AMEX,1", "AMEX,1", "MASTERCARD,5"]


@pytest.mark.part3
@pytest.mark.edge
def test_masked_no_result_and_single_star_positions(impl):
    assert impl.part3(["5482334509943*"]) == []            # 14 digits: no network
    assert impl.part3(["*242424242424242"]) == ["VISA,1"]  # masked prefix: only 4 works
    assert impl.part3(["4242424242424*4*"]) == ["VISA,10"]  # one free digit + one check digit
    assert impl.part3(["*"]) == []


@pytest.mark.part3
@pytest.mark.fmt
def test_masked_multiple_networks_alphabetical(impl):
    assert impl.part3(["*****42424242424"]) == ["MASTERCARD,500", "VISA,1000"]
    assert impl.part3(["*****4242424242"]) == ["AMEX,200"]


@pytest.mark.part3
@pytest.mark.edge
def test_masked_dp_matches_brute_force(impl):
    # Fully independent oracle: its own Luhn (sum-of-digits-of-2d formulation), its own explicit
    # prefix table, and plain enumeration of every '*' completion. Nothing here calls impl.*.
    def oracle_luhn(card):
        total = 0
        for i, ch in enumerate(reversed(card)):
            d = int(ch)
            total += d if i % 2 == 0 else sum(int(x) for x in str(2 * d))
        return total % 10 == 0

    def oracle_network(card):
        if len(card) == 16 and card[0] == "4":
            return "VISA"
        if len(card) == 16 and card[:2] in ("51", "52", "53", "54", "55"):
            return "MASTERCARD"
        if len(card) == 15 and card[:2] in ("34", "37"):
            return "AMEX"
        return None

    def brute(m):
        stars = [i for i, c in enumerate(m) if c == "*"]
        out = {}
        for combo in itertools.product("0123456789", repeat=len(stars)):
            l = list(m)
            for i, d in zip(stars, combo):
                l[i] = d
            c = "".join(l)
            n = oracle_network(c)
            if n and oracle_luhn(c):
                out[n] = out.get(n, 0) + 1
        return out

    # sanity-check the oracle on known cards so a broken oracle cannot silently agree with impl
    assert oracle_luhn("4242424242424242") and not oracle_luhn("4242424242424241")
    assert brute("4242424242424*42") == {"VISA": 1} and brute("5*5555555555444*") == {"MASTERCARD": 5}

    rng = random.Random(5)
    nonempty = 0
    for _ in range(200):
        length = rng.choice([15, 16])
        lead = rng.choice(["4", "5", "3", rng.choice("0123456789")])   # bias toward real prefixes
        digits = lead + "".join(rng.choice("0123456789") for _ in range(length - 1))
        k = rng.randint(1, 4)
        pos = set(rng.sample(range(length), k))
        m = "".join("*" if i in pos else c for i, c in enumerate(digits))
        expected = brute(m)
        nonempty += bool(expected)
        assert impl.masked_counts(m) == expected, m
    assert nonempty >= 50                     # the comparison is not just {} == {}
    assert impl.masked_counts("4242*24*4*42*4*2") == brute("4242*24*4*42*4*2")  # five stars


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example4_verbatim(impl):
    assert impl.part4(["4532015112830367?"]) == P4_SAMPLE_OUT


@pytest.mark.part4
@pytest.mark.fmt
def test_example5_cross_network_numeric_order(impl):
    out = impl.part4(["5242424242424242?"])
    assert out[0] == "4242424242424242,VISA"
    assert out[1] == "5242424242424249,MASTERCARD" and out[-1] == "5272424242424242,MASTERCARD"
    assert len(out) == 15 and all(o.endswith("MASTERCARD") for o in out[1:])
    assert [int(o.split(",")[0]) for o in out] == sorted(int(o.split(",")[0]) for o in out)


@pytest.mark.part4
@pytest.mark.edge
def test_valid_observed_card_has_no_originals(impl):
    assert impl.part4(["4242424242424242?"]) == []
    assert impl.part4(["378282246310005?"]) == []


@pytest.mark.part4
@pytest.mark.edge
def test_swap_and_change_deduped_and_equal_swap_ignored(impl):
    # 4242424242424241? -> the change 1->2 gives 4242424242424242; no swap produces it twice
    out = impl.part4(["4242424242424241?"])
    assert "4242424242424242,VISA" in out and len(out) == len(set(out)) == 15
    # 4422424242424242? -> swap "42"->"24" at the front recovers 4242424242424242
    out = impl.part4(["4422424242424242?"])
    assert out[0] == "4242424242424242,VISA" and len(out) == len(set(out))
    # 4400000000000000?: '00' swaps are identity and must not be listed; the observed card itself never is
    out = impl.part4(["4400000000000000?"])
    assert "4400000000000000,VISA" not in out and len(out) == len(set(out))


@pytest.mark.part4
@pytest.mark.edge
def test_recover_wrong_length_yields_nothing(impl):
    assert impl.part4(["42424242424242?"]) == []
    assert impl.part4([]) == []


# ---------------------------------------------------------------- io / perf
@pytest.mark.part4
@pytest.mark.io
def test_stdin_hackerrank_protocol_exact(run_script):
    r = run_script(HACKERRANK_SAMPLE)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(HACKERRANK_SAMPLE_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_part_protocol(run_script):
    r = run_script("PART 3\n4242424242424*42\n\n5*5555555555444*\n")
    assert r.stdout == "VISA,1\nMASTERCARD,5\n"
    r = run_script("PART 4\n4242424242424242?\n")
    assert r.returncode == 0 and r.stdout == ""
    r = run_script("PART 2\n4111111111111111\n")
    assert r.stdout == "VISA\n"


@pytest.mark.part4
@pytest.mark.io
def test_stdin_bare_lines_infer_part_by_shape(run_script):
    # no PART header, no Pk tag: '?' -> Part 4, '*' -> Part 3, plain 15/16 digits -> Part 2
    r = run_script("4242424242424242\n4242424242424*42\n4532015112830367?\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "VISA\nVISA,1\n" + "\n".join(P4_SAMPLE_OUT) + "\n"
    r = run_script("4242424242424242\n4242424242424241\n")   # the reviewer's crashing input
    assert r.returncode == 0 and r.stdout == "VISA\nINVALID_CHECKSUM\n"


@pytest.mark.part4
@pytest.mark.perf
def test_perf_thousands_of_masked_and_corrupted_queries(run_script):
    rng = random.Random(0)
    lines = []
    for _ in range(1500):
        digits = [rng.choice("0123456789") for _ in range(16)]
        for i in rng.sample(range(16), 5):
            digits[i] = "*"
        lines.append("P3 " + "".join(digits))
    for _ in range(1500):
        lines.append("P4 " + rng.choice("45") + "".join(rng.choice("0123456789") for _ in range(15)) + "?")
    r = run_script(f"{len(lines)}\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
