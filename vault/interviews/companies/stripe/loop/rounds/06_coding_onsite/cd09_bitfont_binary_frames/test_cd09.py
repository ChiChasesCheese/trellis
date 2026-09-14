import random

import pytest

RAW_PAYLOAD = bytes([0b11000000, 0, 0, 0, 0, 0, 0, 0b00000011])
RAW_GRID = [
    [1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1],
]

RLE_ALL_OFF_PAYLOAD = bytes([64, 0])
RLE_STRIPES_PAYLOAD = bytes([8, 1, 8, 0, 8, 1, 8, 0, 8, 1, 8, 0, 8, 1, 8, 0])

COMPACT_PAYLOAD = bytes([0b11110000, 0b10100000, 0, 0])
COMPACT_GRID = [
    [1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

TWO_FRAME_STREAM = bytes([0x00, 0x08, 0x00]) + bytes([0xFF] * 8) + bytes([0x00, 0x02, 0x01]) + bytes([64, 0])


# ---------------------------------------------------------------- Part 1: glyph decoder
@pytest.mark.part1
def test_raw_glyph(impl):
    assert impl.part1(RAW_PAYLOAD, 0) == RAW_GRID


@pytest.mark.part1
def test_rle_all_off_glyph(impl):
    assert impl.part1(RLE_ALL_OFF_PAYLOAD, 1) == [[0] * 8 for _ in range(8)]


@pytest.mark.part1
def test_rle_stripes_glyph(impl):
    grid = impl.part1(RLE_STRIPES_PAYLOAD, 1)
    for r in range(8):
        expected_row = [1] * 8 if r % 2 == 0 else [0] * 8
        assert grid[r] == expected_row


@pytest.mark.part1
def test_compact_glyph(impl):
    assert impl.part1(COMPACT_PAYLOAD, 2) == COMPACT_GRID


@pytest.mark.part1
@pytest.mark.edge
def test_rle_and_compact_both_set_raises(impl):
    with pytest.raises(ValueError):
        impl.part1(b"\x00" * 4, 0b11)


@pytest.mark.part1
@pytest.mark.edge
def test_raw_wrong_length_raises(impl):
    with pytest.raises(ValueError):
        impl.part1(b"\x00" * 7, 0)


@pytest.mark.part1
@pytest.mark.edge
def test_rle_total_not_64_raises(impl):
    with pytest.raises(ValueError):
        impl.part1(bytes([32, 1]), 1)  # only 32 pixels, needs 64


@pytest.mark.part1
@pytest.mark.edge
def test_compact_wrong_length_raises(impl):
    with pytest.raises(ValueError):
        impl.part1(b"\x00" * 3, 2)


# ---------------------------------------------------------------- Part 2: stream/frame decoder
@pytest.mark.part2
def test_two_frame_stream(impl):
    assert impl.part2(TWO_FRAME_STREAM) == [(0, bytes([0xFF] * 8)), (1, bytes([64, 0]))]


@pytest.mark.part2
@pytest.mark.edge
def test_empty_stream_is_empty_list(impl):
    assert impl.part2(b"") == []


@pytest.mark.part2
@pytest.mark.edge
def test_partial_header_raises_eof(impl):
    with pytest.raises(EOFError):
        impl.part2(bytes([0x00, 0x08]))  # only 2 header bytes, need 3


@pytest.mark.part2
@pytest.mark.edge
def test_truncated_payload_raises_eof(impl):
    with pytest.raises(EOFError):
        impl.part2(bytes([0x00, 0x08, 0x00]) + bytes([0xFF] * 5))  # promised 8, only 5 left


@pytest.mark.part2
@pytest.mark.edge
def test_zero_length_payload_frame_parses_without_validating_glyph(impl):
    # a LEN=0 frame is legal *framing* even though flags=0 (raw) would later fail glyph decode --
    # part2 must not itself validate glyph semantics.
    data = bytes([0x00, 0x00, 0x00])
    assert impl.part2(data) == [(0, b"")]


@pytest.mark.part2
def test_three_frames_mixed_flags_in_order(impl):
    stream = TWO_FRAME_STREAM + bytes([0x00, 0x04, 0x02]) + COMPACT_PAYLOAD
    frames = impl.part2(stream)
    assert [f[0] for f in frames] == [0, 1, 2]
    assert frames[2] == (2, COMPACT_PAYLOAD)


# ---------------------------------------------------------------- Part 3: compose
@pytest.mark.part3
def test_compose_two_frame_stream(impl):
    glyphs = impl.part3(TWO_FRAME_STREAM)
    assert glyphs == [[[1] * 8 for _ in range(8)], [[0] * 8 for _ in range(8)]]


@pytest.mark.part3
def test_compose_empty_stream(impl):
    assert impl.part3(b"") == []


@pytest.mark.part3
def test_compose_single_compact_frame(impl):
    stream = bytes([0x00, 0x04, 0x02]) + COMPACT_PAYLOAD
    assert impl.part3(stream) == [COMPACT_GRID]


@pytest.mark.part3
@pytest.mark.edge
def test_compose_propagates_glyph_validation_error(impl):
    # framing succeeds (LEN=7 is a valid frame), but the payload is invalid for flags=0 (raw)
    stream = bytes([0x00, 0x07, 0x00]) + bytes([0xFF] * 7)
    with pytest.raises(ValueError):
        impl.part3(stream)


# ---------------------------------------------------------------- fmt
@pytest.mark.part1
@pytest.mark.fmt
def test_stdout_grid_is_zero_one_digit_string_msb_first(run_script):
    r = run_script("PART 1\n0 " + RAW_PAYLOAD.hex() + "\n")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "11000000"
    assert lines[-1] == "00000011"
    assert len(lines) == 8


@pytest.mark.part2
@pytest.mark.fmt
def test_stdout_hex_is_lowercase_and_zero_padded(run_script):
    # payload byte 0x0a must render "0a", not "a" or "0A"
    stream = bytes([0x00, 0x01, 0x00, 0x0A])
    r = run_script("PART 2\n" + stream.hex() + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0 0a\n"


# ---------------------------------------------------------------- io
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3_blank_line_between_glyphs(run_script):
    r = run_script("PART 3\n" + TWO_FRAME_STREAM.hex() + "\n")
    assert r.returncode == 0, r.stderr
    expected_glyph1 = "\n".join("1" * 8 for _ in range(8))
    expected_glyph2 = "\n".join("0" * 8 for _ in range(8))
    assert r.stdout == expected_glyph1 + "\n\n" + expected_glyph2 + "\n"


# ---------------------------------------------------------------- perf
@pytest.mark.part3
@pytest.mark.perf
def test_perf_many_frames(run_script):
    rng = random.Random(0)
    frames = []
    for _ in range(20000):
        payload = bytes(rng.getrandbits(8) for _ in range(8))
        frames.append(bytes([0x00, 0x08, 0x00]) + payload)
    stream = b"".join(frames)
    r = run_script("PART 3\n" + stream.hex() + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 5.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
    blocks = r.stdout.split("\n\n")
    assert len(blocks) == 20000
