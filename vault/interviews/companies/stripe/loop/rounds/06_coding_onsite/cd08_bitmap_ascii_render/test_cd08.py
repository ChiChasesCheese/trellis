import json

import pytest

FONT = {"A": "010101111101101", "B": "110101110101110"}
WIDTH, HEIGHT = 3, 5

EXAMPLE1_OUT = [
    ".#..##.",
    "#.#.#.#",
    "###.##.",
    "#.#.#.#",
    "#.#.##.",
]
EXAMPLE2_OUT = [
    ".#.......#.",
    "#.#.....#.#",
    "###.....###",
    "#.#.....#.#",
    "#.#.....#.#",
]


# ---------------------------------------------------------------- Part 1: single glyph decode
@pytest.mark.part1
def test_example1_glyph_A(impl):
    assert impl.part1(FONT["A"], WIDTH, HEIGHT) == [".#.", "#.#", "###", "#.#", "#.#"]


@pytest.mark.part1
def test_example1_glyph_B(impl):
    assert impl.part1(FONT["B"], WIDTH, HEIGHT) == ["##.", "#.#", "##.", "#.#", "##."]


@pytest.mark.part1
def test_all_zero_and_all_one_glyphs(impl):
    assert impl.part1("0" * 6, 2, 3) == ["..", "..", ".."]
    assert impl.part1("1" * 6, 2, 3) == ["##", "##", "##"]


@pytest.mark.part1
@pytest.mark.edge
def test_glyph_wrong_length_raises(impl):
    with pytest.raises(ValueError):
        impl.part1("010", WIDTH, HEIGHT)  # too short for 3*5=15


# ---------------------------------------------------------------- Part 2: happy-path layout
@pytest.mark.part2
def test_example1_render_AB(impl):
    assert impl.part2(FONT, WIDTH, HEIGHT, "AB") == EXAMPLE1_OUT


@pytest.mark.part2
def test_example2_render_A_space_A(impl):
    assert impl.part2(FONT, WIDTH, HEIGHT, "A A") == EXAMPLE2_OUT


@pytest.mark.part2
def test_single_char_no_separator(impl):
    out = impl.part2(FONT, WIDTH, HEIGHT, "A")
    assert out == [".#.", "#.#", "###", "#.#", "#.#"]
    assert all(len(row) == WIDTH for row in out)


@pytest.mark.part2
def test_repeated_characters_render_identically(impl):
    out = impl.part2(FONT, WIDTH, HEIGHT, "AAAA")
    glyph_a = impl.part1(FONT["A"], WIDTH, HEIGHT)
    # each of the 4 glyph slots (width 3, separated by 1 '.' column) must equal glyph_a exactly
    for row_idx, row in enumerate(out):
        assert len(row) == WIDTH * 4 + 3
        for slot in range(4):
            start = slot * (WIDTH + 1)
            assert row[start : start + WIDTH] == glyph_a[row_idx]


# ---------------------------------------------------------------- Part 3: full contract + validation
@pytest.mark.part3
def test_part3_matches_part2_on_valid_input(impl):
    assert impl.part3(FONT, WIDTH, HEIGHT, "AB") == EXAMPLE1_OUT
    assert impl.part3(FONT, WIDTH, HEIGHT, "A A") == EXAMPLE2_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_part3_missing_character_raises(impl):
    with pytest.raises(ValueError):
        impl.part3(FONT, WIDTH, HEIGHT, "AC")


@pytest.mark.part3
@pytest.mark.edge
def test_part3_invalid_length_font_entry_raises(impl):
    bad_font = {"A": "0101"}  # needs 15 bits, only has 4
    with pytest.raises(ValueError):
        impl.part3(bad_font, WIDTH, HEIGHT, "A")


@pytest.mark.part3
def test_part3_moderate_length_text_correctness(impl):
    out = impl.part3(FONT, WIDTH, HEIGHT, "ABAB")
    assert len(out) == HEIGHT
    assert all(len(row) == WIDTH * 4 + 3 for row in out)
    # each half should independently match the AB example (concatenated with a separator)
    assert out == [row1 + "." + row2 for row1, row2 in zip(EXAMPLE1_OUT, EXAMPLE1_OUT)]


# ---------------------------------------------------------------- fmt
@pytest.mark.part3
@pytest.mark.fmt
def test_space_is_always_blank_even_if_font_has_space_key(impl):
    distractor_font = dict(FONT)
    distractor_font[" "] = "1" * (WIDTH * HEIGHT)  # should never be consulted
    out = impl.part3(distractor_font, WIDTH, HEIGHT, "A A")
    assert out == EXAMPLE2_OUT


@pytest.mark.part2
@pytest.mark.fmt
def test_row_lengths_and_count_are_exact(impl):
    out = impl.part2(FONT, WIDTH, HEIGHT, "AB")
    assert len(out) == HEIGHT
    assert all(len(row) == WIDTH * 2 + 1 for row in out)


# ---------------------------------------------------------------- io
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3_exact(run_script):
    payload = {"font": FONT, "width": WIDTH, "height": HEIGHT, "text": "AB"}
    r = run_script("PART 3\n" + json.dumps(payload) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EXAMPLE1_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1_exact(run_script):
    payload = {"bitstring": FONT["A"], "width": WIDTH, "height": HEIGHT}
    r = run_script("PART 1\n" + json.dumps(payload) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join([".#.", "#.#", "###", "#.#", "#.#"]) + "\n"


# ---------------------------------------------------------------- perf
@pytest.mark.part3
@pytest.mark.perf
def test_perf_long_text(run_script):
    import string

    letters = string.ascii_lowercase + " "
    w, h = 5, 7
    font = {ch: "0" * (w * h) for ch in letters if ch != " "}
    text = "".join(letters[i % len(letters)] for i in range(10000))
    payload = {"font": font, "width": w, "height": h, "text": text}
    r = run_script("PART 3\n" + json.dumps(payload) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
    lines = r.stdout.strip("\n").split("\n")
    assert len(lines) == h
    assert len(lines[0]) == len(text) * w + (len(text) - 1)
