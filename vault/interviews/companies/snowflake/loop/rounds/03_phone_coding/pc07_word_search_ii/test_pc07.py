import random

import pytest

BOARD1 = ["oaan", "etae", "ihkr", "iflv"]
WORDS1 = ["oath", "pea", "eat", "rain"]

BOARD3 = ["abce", "sfcs", "adee"]
WORDS3 = ["abcced", "see", "abcb"]


def _grid(rows: list[str]) -> list[list[str]]:
    return [list(row) for row in rows]


def _brute_find(board, words):
    """Reference-independent brute force: DFS every start cell, no trie, no pruning."""
    rows, cols = len(board), len(board[0])
    dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def dfs(r, c, word, i, visited):
        if board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        visited.add((r, c))
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if dfs(nr, nc, word, i + 1, visited):
                    visited.discard((r, c))
                    return True
        visited.discard((r, c))
        return False

    found = set()
    for w in words:
        if any(dfs(r, c, w, 0, set()) for r in range(rows) for c in range(cols)):
            found.add(w)
    return sorted(found)


def _random_board(rng, rows, cols, alphabet="abc"):
    return [[rng.choice(alphabet) for _ in range(cols)] for _ in range(rows)]


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.find_words(_grid(BOARD1), WORDS1) == ["eat", "oath"]


@pytest.mark.part1
def test_worked_example_2_none_found(impl):
    assert impl.find_words(_grid(["ab", "cd"]), ["abcb"]) == []


@pytest.mark.part1
def test_worked_example_3(impl):
    assert impl.find_words(_grid(BOARD3), WORDS3) == ["abcced", "see"]


@pytest.mark.part1
@pytest.mark.edge
def test_single_cell_cannot_reuse(impl):
    assert impl.find_words(_grid(["a"]), ["a", "aa"]) == ["a"]


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_word_counted_once(impl):
    assert impl.find_words(_grid(BOARD1), ["oath", "oath"]) == ["oath"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_words_list(impl):
    assert impl.find_words(_grid(BOARD1), []) == []


@pytest.mark.part1
@pytest.mark.edge
def test_invalid_board_raises(impl):
    with pytest.raises(ValueError):
        impl.find_words([], ["a"])
    with pytest.raises(ValueError):
        impl.find_words([["a", "b"], ["c"]], ["a"])
    with pytest.raises(ValueError):
        impl.find_words([["A"]], ["a"])


@pytest.mark.part1
@pytest.mark.edge
def test_invalid_word_raises(impl):
    with pytest.raises(ValueError):
        impl.find_words([["a"]], ["A"])
    with pytest.raises(ValueError):
        impl.find_words([["a"]], [""])


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(60):
        rows, cols = rng.randint(1, 4), rng.randint(1, 4)
        board = _random_board(rng, rows, cols)
        words = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 4))) for _ in range(5)]
        assert impl.find_words(board, words) == _brute_find(board, words), (board, words)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_worked_example_1(impl):
    assert impl.find_words_with_paths(_grid(BOARD1), WORDS1) == [
        ("eat", [(1, 3), (1, 2), (1, 1)]),
        ("oath", [(0, 0), (0, 1), (1, 1), (2, 1)]),
    ]


@pytest.mark.part2
def test_part2_worked_example_3(impl):
    assert impl.find_words_with_paths(_grid(BOARD3), WORDS3) == [
        ("abcced", [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1)]),
        ("see", [(1, 3), (2, 3), (2, 2)]),
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_first_path_is_row_major_start_then_udlr(impl):
    assert impl.find_words_with_paths(_grid(["aa"]), ["aa"]) == [("aa", [(0, 0), (0, 1)])]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_none_found(impl):
    assert impl.find_words_with_paths(_grid(["ab", "cd"]), ["abcb"]) == []


@pytest.mark.part2
@pytest.mark.edge
def test_part2_path_matches_board_letters_and_is_adjacent(impl):
    rng = random.Random(1)
    for _ in range(60):
        rows, cols = rng.randint(1, 4), rng.randint(1, 4)
        board = _random_board(rng, rows, cols)
        words = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 4))) for _ in range(5)]
        pairs = impl.find_words_with_paths(board, words)
        found_words = sorted(w for w, _ in pairs)
        assert found_words == _brute_find(board, words)
        for w, path in pairs:
            assert len(path) == len(w)
            assert len(set(path)) == len(path)
            for (r, c), ch in zip(path, w):
                assert board[r][c] == ch
            for (r0, c0), (r1, c1) in zip(path, path[1:]):
                assert abs(r0 - r1) + abs(c0 - c1) == 1


@pytest.mark.part2
@pytest.mark.fmt
def test_part2_output_lines(impl):
    assert impl.part2(["1 2", "aa", "W 1", "aa"]) == ["aa 0,0 0,1"]
    assert impl.part2(["2 2", "ab", "cd", "W 1", "abcb"]) == ["-"]


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_12x12_30000_words(run_script):
    rng = random.Random(0)
    rows, cols = 12, 12
    board_alphabet = "abcdef"
    board = ["".join(rng.choice(board_alphabet) for _ in range(cols)) for _ in range(rows)]
    words = set()
    while len(words) < 30_000:
        length = rng.randint(2, 6)
        words.add("".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(length)))
    lines = [f"{rows} {cols}", *board, f"W {len(words)}", *sorted(words)]
    r = run_script("PART 1\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script(
        "PART 1\n4 4\noaan\netae\nihkr\niflv\nW 4\noath\npea\neat\nrain\n"
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout == "eat oath\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n1 2\naa\nW 1\naa\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "aa 0,0 0,1\n"
