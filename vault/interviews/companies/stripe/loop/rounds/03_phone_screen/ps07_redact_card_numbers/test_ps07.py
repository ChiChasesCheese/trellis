import random

import pytest


# ---------------------------------------------------------------- Part 1: bare digit runs
@pytest.mark.part1
def test_example_bare_pan(impl):
    assert impl.part1(["user 4242424242424242 charged $10"]) == ["user ************4242 charged $10"]


@pytest.mark.part1
@pytest.mark.edge
def test_boundary_lengths(impl):
    # 13 and 19 digits both count; 12 and 20 do not (never partially masked)
    assert impl.part1(["4000000000006", "4000000000000000006", "123456789012", "12345678901234567890"]) == [
        "*********0006",
        "***************0006",
        "123456789012",
        "12345678901234567890",
    ]


@pytest.mark.part1
@pytest.mark.edge
def test_over_redaction_timestamp(impl):
    # Part 1 has no Luhn/brand filter yet -- a 13-digit unix-ms timestamp gets wrongly redacted.
    # This is intentional and is exactly what Part 3 fixes.
    assert impl.part1(['{"ts":1735689600000,"event":"login"}']) == ['{"ts":*********0000,"event":"login"}']


@pytest.mark.part1
def test_blank_lines_and_line_count_preserved(impl):
    out = impl.part1(["", "4242424242424242", ""])
    assert len(out) == 3
    assert out[0] == ""
    assert out[1] == "************4242"
    assert out[2] == ""


@pytest.mark.part1
def test_no_digits_untouched(impl):
    assert impl.part1(["no card numbers here at all"]) == ["no card numbers here at all"]


@pytest.mark.part1
@pytest.mark.edge
def test_punctuation_boundary_no_whitespace(impl):
    # non-digit boundary can be punctuation, not just whitespace
    assert impl.part1(["id=4242424242424242;"]) == ["id=************4242;"]


# ---------------------------------------------------------------- Part 2: separators
@pytest.mark.part2
def test_example_formatted(impl):
    assert impl.part2(
        [
            "Card: 4111-1111-1111-1111 charged $50",
            "Card: 4111 1111 1111 1111 charged $50",
        ]
    ) == [
        "Card: ****-****-****-1111 charged $50",
        "Card: **** **** **** 1111 charged $50",
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_five_group_chain_too_long_untouched(impl):
    # 20 digits total across 5 groups -- out of range, never partially masked
    assert impl.part2(["4111-1111-1111-1111-2222"]) == ["4111-1111-1111-1111-2222"]


@pytest.mark.part2
@pytest.mark.edge
def test_over_grouping_across_phone_number(impl):
    # naive space/'-'-joining splices an unrelated phone number into one 13-digit candidate;
    # this over-redaction is intentional here and is fixed in Part 3
    assert impl.part2(["call +86 138 0013 8000 now"]) == ["call +** *** **** 8000 now"]


@pytest.mark.part2
@pytest.mark.edge
def test_doubled_separator_breaks_the_chain(impl):
    # "4111--1111-1111-1111" has a doubled '-' -- the chain stops at the break, each side is
    # too short on its own (4 and 12 digits) to be a candidate at all
    assert impl.part2(["4111--1111-1111-1111"]) == ["4111--1111-1111-1111"]


@pytest.mark.part2
@pytest.mark.edge
def test_leading_and_trailing_separator_excluded(impl):
    # the leading/trailing '-' is not consumed by the scanner (a chain only starts/ends on a
    # digit), so it stays as literal text and the digit chain is still redacted in full
    assert impl.part2(["-4111 1111 1111 1111"]) == ["-**** **** **** 1111"]
    assert impl.part2(["4111 1111 1111 1111-"]) == ["**** **** **** 1111-"]


@pytest.mark.part2
@pytest.mark.fmt
def test_last4_counts_digits_not_characters(impl):
    # AMEX grouping 4-6-5: last 4 *digits* land inside the final 5-digit group
    out = impl.part2(["amex 3782-822463-10005 charged"])
    assert out == ["amex ****-******-*0005 charged"]


# ---------------------------------------------------------------- Part 3: Luhn + brand filter
@pytest.mark.part3
def test_fixes_false_positives(impl):
    assert impl.part3(
        [
            '{"ts":1735689600000,"event":"login"}',
            "call +86 138 0013 8000 now",
            "order 1234567890123456 shipped",
        ]
    ) == [
        '{"ts":1735689600000,"event":"login"}',
        "call +86 138 0013 8000 now",
        "order 1234567890123456 shipped",
    ]


@pytest.mark.part3
def test_real_pans_redacted_including_networks_q05_lacks(impl):
    assert impl.part3(
        [
            "mc old range 5555555555554444 refund",
            "mc new range 2223003122003222 refund",
            "discover 6011111111111117 refund",
            "amex 378282246310005 refund",
            "bad checksum 4242424242424241 refund",
        ]
    ) == [
        "mc old range ************4444 refund",
        "mc new range ************3222 refund",
        "discover ************1117 refund",
        "amex ***********0005 refund",
        "bad checksum 4242424242424241 refund",
    ]


@pytest.mark.part3
@pytest.mark.edge
def test_wrong_prefix_right_length_untouched(impl):
    # 16 digits, prefix '9' matches no network
    assert impl.part3(["9242424242424242"]) == ["9242424242424242"]


@pytest.mark.part3
@pytest.mark.edge
def test_right_length_prefix_wrong_luhn_untouched(impl):
    assert impl.part3(["4242424242424241"]) == ["4242424242424241"]


@pytest.mark.part3
@pytest.mark.edge
def test_mixed_line_partial_redaction(impl):
    out = impl.part3(["real 4242424242424242 fake 1234567890123456 real 378282246310005"])
    assert out == ["real ************4242 fake 1234567890123456 real ***********0005"]


@pytest.mark.part3
@pytest.mark.edge
def test_separated_pan_is_validated_on_its_digits(impl):
    # Luhn/brand run on the concatenated digits, masking still keeps the separators
    out = impl.part3(["4242 4242 4242 4242 ok", "4242 4242 4242 4241 bad"])
    assert out == ["**** **** **** 4242 ok", "4242 4242 4242 4241 bad"]


@pytest.mark.part3
@pytest.mark.edge
def test_pan_chained_to_a_neighbouring_number_is_left_alone_by_design(impl):
    # "12 4242424242424242" is one 18-digit chain -> no brand -> untouched (maximal-chain contract)
    assert impl.part3(["ref 12 4242424242424242"]) == ["ref 12 4242424242424242"]


@pytest.mark.part3
def test_direct_luhn_and_brand_helpers(impl):
    assert impl.luhn_ok("4242424242424242") is True
    assert impl.luhn_ok("4242424242424241") is False
    assert impl.brand_of("2223003122003222") == "MASTERCARD"
    assert impl.brand_of("6011111111111117") == "DISCOVER"
    assert impl.brand_of("1234567890123456") is None
    assert impl.is_card_number("378282246310005") is True
    assert impl.is_card_number("1735689600000") is False  # wrong length too (13, no brand)


# ---------------------------------------------------------------- Part 4: streaming + stats
@pytest.mark.part4
def test_example_multi_card_with_stats(impl):
    assert impl.part4(["4242424242424242 and 5555555555554444 both charged", "not a card: 42 42"]) == [
        "************4242 and ************4444 both charged",
        "not a card: 42 42",
        "REDACTED 2",
    ]


@pytest.mark.part4
@pytest.mark.edge
def test_stats_zero_when_nothing_redacted(impl):
    assert impl.part4(["order 1234567890123456 shipped", "no cards here"]) == [
        "order 1234567890123456 shipped",
        "no cards here",
        "REDACTED 0",
    ]


@pytest.mark.part4
def test_empty_body_still_prints_stats_line(impl):
    assert impl.part4([]) == ["REDACTED 0"]


@pytest.mark.part4
@pytest.mark.edge
def test_three_cards_one_line(impl):
    line = "4242424242424242,5555555555554444,378282246310005"
    out = impl.part4([line])
    assert out == ["************4242,************4444,***********0005", "REDACTED 3"]


# ---------------------------------------------------------------- io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nuser 4242424242424242 charged $10\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "user ************4242 charged $10\n"


@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_part4(run_script):
    stdin = "PART 4\n4242424242424242 and 5555555555554444 both charged\nnot a card: 42 42\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == (
        "************4242 and ************4444 both charged\n" "not a card: 42 42\n" "REDACTED 2\n"
    )


@pytest.mark.part1
@pytest.mark.io
def test_stdin_empty(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part1
@pytest.mark.io
def test_blank_body_lines_round_trip_through_stdin(run_script):
    r = run_script("PART 1\nfirst\n\nlast\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "first\n\nlast\n"


# ---------------------------------------------------------------- perf
@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_lines(run_script):
    rng = random.Random(0)
    real_pans = [
        "4242424242424242",
        "5555555555554444",
        "378282246310005",
        "6011111111111117",
        "2223003122003222",
    ]
    lines = []
    for i in range(100_000):
        if i % 500 == 0:
            pan = rng.choice(real_pans)
            lines.append(f"line {i}: charge {pan} succeeded")
        elif i % 137 == 0:
            # a look-alike (timestamp-shaped) that must survive untouched
            lines.append(f'line {i}: {{"ts":{1_700_000_000_000 + i},"ok":true}}')
        else:
            lines.append(f"line {i}: nothing to see here, order {1000 + i} shipped")
    stdin = "PART 4\n" + "\n".join(lines) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    out_lines = r.stdout.splitlines()
    assert out_lines[-1].startswith("REDACTED ")
    redacted_count = int(out_lines[-1].split()[1])
    expected = sum(1 for i in range(100_000) if i % 500 == 0)
    assert redacted_count == expected
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
