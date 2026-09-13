import random

import pytest

TEXT = "The quick brown fox is quick and the lazy dog sleeps while a quick cat runs far away from the quick fox"


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_source_1_20(impl):
    assert impl.find_starts(TEXT, "quick fox", 2) == [1, 20]


@pytest.mark.part1
@pytest.mark.edge
def test_k_boundary_and_order(impl):
    assert impl.find_starts(TEXT, "quick fox", 1) == [20]     # distance 2 excluded at k=1
    assert impl.find_starts(TEXT, "quick fox", 2) == [1, 20]  # distance exactly k counts
    assert impl.find_starts(TEXT, "fox quick", 2) == [3]      # other word must come AFTER
    assert impl.find_starts(TEXT, "quick", 0) == [1, 5, 13, 20]
    assert impl.find_starts(TEXT, "quick fox", 0) == []


@pytest.mark.part1
@pytest.mark.edge
def test_absent_empty_and_duplicates(impl):
    assert impl.find_starts(TEXT, "zebra fox", 5) == []
    assert impl.find_starts(TEXT, "fox zebra", 100) == []
    assert impl.find_starts("", "quick", 3) == []
    assert impl.find_starts(TEXT, "", 3) == []
    assert impl.find_starts(TEXT, "quick quick fox", 2) == [1, 20]  # duplicate query word ignored
    assert impl.find_starts("a b c a", "a b c", 2) == [0]


@pytest.mark.part1
def test_document_reuse_and_process_format(impl):
    d = impl.Document(TEXT)
    assert d.positions["fox"] == [3, 21]
    assert impl.find_starts(d, "quick fox", 2) == [1, 20]
    assert impl.process([TEXT, "quick fox|2", "zebra fox|5", "quick|0"], 1) == ["1 20", "", "1 5 13 20"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_min_window(impl):
    assert impl.min_window(TEXT, "quick fox") == (20, 21)
    assert impl.min_window(TEXT, "lazy cat") == (8, 14)
    assert impl.min_window(TEXT, "quick zebra") is None
    assert impl.process([TEXT, "quick fox", "lazy cat", "quick zebra"], 2) == ["20,21", "8,14", "-1"]


@pytest.mark.part2
@pytest.mark.edge
def test_min_window_ties_repeats_single(impl):
    assert impl.min_window("a b x a b", "a b") == (0, 1)        # tie -> earliest
    assert impl.min_window("a x x b x a b", "a b") == (5, 6)    # later but shorter wins
    assert impl.min_window("quick quick fox", "quick fox") == (1, 2)
    assert impl.min_window("fox", "fox") == (0, 0)
    assert impl.min_window("", "fox") is None
    assert impl.min_window("a b", "") is None


@pytest.mark.part2
def test_min_window_matches_brute_force(impl):
    rng = random.Random(0)
    for _ in range(150):
        toks = [rng.choice("abcd") for _ in range(rng.randrange(0, 10))]
        q = " ".join(rng.sample("abcd", rng.randrange(1, 4)))
        need = set(q.split())
        best = None
        for i in range(len(toks)):
            for j in range(i, len(toks)):
                if need <= set(toks[i:j + 1]) and (best is None or j - i < best[1] - best[0]):
                    best = (i, j)
        assert impl.min_window(" ".join(toks), q) == best


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_normalization(impl):
    text = "The Quick, brown fox! Quick-fox."
    assert impl.tokenize(text, normalize=True) == ["the", "quick", "brown", "fox", "quick", "fox"]
    assert impl.min_window(text, "QUICK fox", normalize=True) == (3, 4)   # "fox quick" (any order)
    assert impl.process([text, "QUICK fox"], 3) == ["3,4"]


@pytest.mark.part3
@pytest.mark.edge
def test_normalization_vs_exact(impl):
    text = "Fox, fox"
    assert impl.min_window(text, "fox") == (1, 1)                    # exact: 'Fox,' != 'fox'
    assert impl.min_window(text, "fox", normalize=True) == (0, 0)
    assert impl.find_starts("a-b c", "a b", 1, normalize=True) == [0]
    assert impl.tokenize("  ", normalize=True) == [] and impl.tokenize("x1 2y", normalize=True) == ["x1", "2y"]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example_rank(impl):
    docs = [("a", "the quick brown fox"), ("b", "fox quick"), ("c", "quick and slow"), ("d", "Quick, fox!")]
    assert impl.rank(docs, "quick fox") == [("b", 2), ("d", 2), ("a", 3)]
    assert impl.process(["quick fox", "a|the quick brown fox", "b|fox quick", "c|quick and slow", "d|Quick, fox!"], 4) == ["b,2", "d,2", "a,3"]


@pytest.mark.part4
@pytest.mark.edge
def test_rank_edges(impl):
    assert impl.rank([], "quick fox") == []
    assert impl.rank([("a", "quick"), ("b", "fox")], "quick fox") == []
    assert impl.rank([("z", "fox quick"), ("a", "fox quick")], "quick fox") == [("z", 2), ("a", 2)]  # input order on tie
    assert impl.rank([("p", "x|y quick fox")], "quick fox") == [("p", 2)]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script(f"PART 1\n{TEXT}\n\nquick fox|2\nquick fox|1\nzebra fox|5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1 20\n20\n\n"
    assert run_script("PART 4\nquick fox\na|the quick brown fox\nb|fox quick\n").stdout == "b,2\na,3\n"
    assert run_script("").stdout == ""


@pytest.mark.part2
@pytest.mark.perf
def test_perf_200k_words_many_queries(run_script):
    rng = random.Random(0)
    vocab = [f"w{i}" for i in range(500)]
    text = " ".join(rng.choice(vocab) for _ in range(200_000))
    queries = [" ".join(rng.sample(vocab, 3)) for _ in range(20)]
    r = run_script("PART 1\n" + text + "\n" + "\n".join(f"{q}|50" for q in queries) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 20
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
    r = run_script("PART 2\n" + text + "\n" + "\n".join(queries) + "\n", timeout=30)
    assert r.stdout.count("\n") == 20 and r.seconds < 2.0
