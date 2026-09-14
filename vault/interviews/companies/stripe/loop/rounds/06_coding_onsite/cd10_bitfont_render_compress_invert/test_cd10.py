import json
import random

import pytest

FONT_A_ROWS = [102, 153, 129, 255, 129, 129, 129, 0]  # 0b01100110, 0b10011001, ... see problem.md
FONT = {"A": FONT_A_ROWS}

RENDER_A = [
    ".##..##.",
    "#..##..#",
    "#......#",
    "########",
    "#......#",
    "#......#",
    "#......#",
    "........",
]

RENDER_A_A_SEP1 = [
    ".##..##............##..##.",
    "#..##..#..........#..##..#",
    "#......#..........#......#",
    "########..........########",
    "#......#..........#......#",
    "#......#..........#......#",
    "#......#..........#......#",
    "..........................",
]

COMPRESS_A = (
    "1:0;2:1;2:0;2:1;1:0|1:1;2:0;2:1;2:0;1:1|1:1;6:0;1:1|8:1" "|1:1;6:0;1:1|1:1;6:0;1:1|1:1;6:0;1:1|8:0"
)

RENDER_A_INVERTED = [
    "#..##..#",
    ".##..##.",
    ".######.",
    "........",
    ".######.",
    ".######.",
    ".######.",
    "########",
]


# ---------------------------------------------------------------- Part 1: Draw One Character
@pytest.mark.part1
def test_render_A(impl):
    assert impl.part1(FONT, "A") == RENDER_A


@pytest.mark.part1
def test_render_all_zero_and_all_one_glyph(impl):
    assert impl.part1({"Z": [0] * 8}, "Z") == ["........"] * 8
    assert impl.part1({"F": [255] * 8}, "F") == ["########"] * 8


@pytest.mark.part1
def test_render_mixed_pattern_glyph(impl):
    # 0b10101010 = 170 -> alternating bits
    assert impl.part1({"X": [170] * 8}, "X") == ["#.#.#.#."] * 8


@pytest.mark.part1
@pytest.mark.edge
def test_render_missing_char_raises_keyerror(impl):
    with pytest.raises(KeyError):
        impl.part1(FONT, "Q")


# ---------------------------------------------------------------- Part 2: Draw a Word
@pytest.mark.part2
def test_render_word_with_space_sep1(impl):
    assert impl.part2(FONT, "A A", sep=1) == RENDER_A_A_SEP1


@pytest.mark.part2
def test_render_word_sep0_glyphs_touch(impl):
    out = impl.part2(FONT, "AA", sep=0)
    assert out[0] == ".##..##..##..##."
    assert all(len(row) == 16 for row in out)


@pytest.mark.part2
def test_render_single_char_word_equals_part1(impl):
    assert impl.part2(FONT, "A", sep=1) == RENDER_A


@pytest.mark.part2
@pytest.mark.edge
def test_render_word_missing_char_propagates_keyerror(impl):
    with pytest.raises(KeyError):
        impl.part2(FONT, "AB")


# ---------------------------------------------------------------- Part 3: Compressed Fonts (RLE)
@pytest.mark.part3
def test_compress_glyph_A(impl):
    assert impl.part3_compress(FONT_A_ROWS) == COMPRESS_A


@pytest.mark.part3
def test_decompress_is_inverse_of_compress(impl):
    assert impl.part3_decompress(COMPRESS_A) == FONT_A_ROWS


@pytest.mark.part3
@pytest.mark.edge
def test_compress_uniform_rows_single_token_each(impl):
    assert impl.part3_compress([0] * 8) == "|".join(["8:0"] * 8)
    assert impl.part3_compress([255] * 8) == "|".join(["8:1"] * 8)


@pytest.mark.part3
def test_roundtrip_property_random_glyphs(impl):
    rng = random.Random(0)
    for _ in range(50):
        rows = [rng.randrange(256) for _ in range(8)]
        assert impl.part3_decompress(impl.part3_compress(rows)) == rows


# ---------------------------------------------------------------- Part 4: Invert
@pytest.mark.part4
def test_invert_A(impl):
    assert impl.part4(FONT, "A") == RENDER_A_INVERTED


@pytest.mark.part4
@pytest.mark.edge
def test_invert_all_zero_glyph_becomes_all_filled(impl):
    assert impl.part4({"Z": [0] * 8}, "Z") == ["########"] * 8


@pytest.mark.part4
@pytest.mark.edge
def test_invert_does_not_mutate_original_font(impl):
    font = {"A": list(FONT_A_ROWS)}
    impl.part4(font, "A")
    assert font["A"] == FONT_A_ROWS


# ---------------------------------------------------------------- fmt
@pytest.mark.part3
@pytest.mark.fmt
def test_compress_token_delimiters_exact(impl):
    # single row test via an 8-row glyph where every row is the same alternating pattern
    out = impl.part3_compress([170] * 8)
    one_row = "1:1;1:0;1:1;1:0;1:1;1:0;1:1;1:0"
    assert out == "|".join([one_row] * 8)


@pytest.mark.part2
@pytest.mark.fmt
def test_word_row_lengths_exact_for_sep(impl):
    out = impl.part2(FONT, "AAA", sep=2)
    assert all(len(row) == 8 * 3 + 2 * 2 for row in out)


# ---------------------------------------------------------------- io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1_exact(run_script):
    payload = {"font": FONT, "ch": "A"}
    r = run_script("PART 1\n" + json.dumps(payload) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(RENDER_A) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3_compress_and_decompress(run_script):
    r1 = run_script("PART 3\n" + json.dumps({"op": "compress", "rows": FONT_A_ROWS}) + "\n")
    assert r1.returncode == 0, r1.stderr
    assert r1.stdout == COMPRESS_A + "\n"

    r2 = run_script("PART 3\n" + json.dumps({"op": "decompress", "s": COMPRESS_A}) + "\n")
    assert r2.returncode == 0, r2.stderr
    assert r2.stdout == ",".join(str(v) for v in FONT_A_ROWS) + "\n"


# ---------------------------------------------------------------- perf
@pytest.mark.part2
@pytest.mark.perf
def test_perf_long_word(run_script):
    rng = random.Random(0)
    alphabet = [chr(ord("a") + i) for i in range(26)] + [" "]
    font = {ch: [rng.randrange(256) for _ in range(8)] for ch in alphabet if ch != " "}
    word = "".join(rng.choice(alphabet) for _ in range(8000))
    payload = {"font": font, "word": word, "sep": 1}
    r = run_script("PART 2\n" + json.dumps(payload) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
    lines = r.stdout.strip("\n").split("\n")
    assert len(lines) == 8
    assert len(lines[0]) == len(word) * 8 + (len(word) - 1)
