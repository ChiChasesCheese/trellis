import random
import re

import pytest

_TOKEN_RE = re.compile(r"\(|\)|[^\s()]+")


def _tokenize(expr):
    return _TOKEN_RE.findall(expr)


class _BruteParser:
    """Independent recursive-descent parser + PER-DOCUMENT (not inverted-index) evaluator, used
    only as a cross-check reference."""

    def __init__(self, tokens):
        self.tokens, self.pos = tokens, 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def adv(self):
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def expr(self):
        node = self.term()
        while self.peek() == "OR":
            self.adv()
            node = ("OR", node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.peek() == "AND":
            self.adv()
            node = ("AND", node, self.factor())
        return node

    def factor(self):
        tok = self.peek()
        if tok == "NOT":
            self.adv()
            return ("NOT", self.factor())
        if tok == "(":
            self.adv()
            node = self.expr()
            assert self.adv() == ")"
            return node
        self.adv()
        return ("WORD", tok)


def _brute_eval(node, doc_words):
    kind = node[0]
    if kind == "WORD":
        return node[1] in doc_words
    if kind == "AND":
        return _brute_eval(node[1], doc_words) and _brute_eval(node[2], doc_words)
    if kind == "OR":
        return _brute_eval(node[1], doc_words) or _brute_eval(node[2], doc_words)
    if kind == "NOT":
        return not _brute_eval(node[1], doc_words)


def _brute_matches(query, docs):
    """docs: dict[int, set[str]] -> sorted list of matching ids, scanning every document
    directly (no inverted index at all)."""
    node = _BruteParser(_tokenize(query)).expr()
    return sorted(doc_id for doc_id, words in docs.items() if _brute_eval(node, words))


def _brute_or_matches(query, docs):
    query_words = set(query.split())
    return sorted(doc_id for doc_id, words in docs.items() if words & query_words)


WORDS = ["cat", "dog", "fish", "bird", "ant"]


def _random_docs(rng, n_docs):
    docs = {}
    for doc_id in range(1, n_docs + 1):
        k = rng.randint(1, 3)
        docs[doc_id] = set(rng.sample(WORDS, k))
    return docs


def _random_bool_query(rng, depth):
    if depth <= 0 or rng.random() < 0.4:
        return rng.choice(WORDS)
    kind = rng.choice(["AND", "OR", "NOT", "PAREN"])
    if kind == "NOT":
        return f"NOT {_random_bool_query(rng, depth - 1)}"
    if kind == "PAREN":
        return f"({_random_bool_query(rng, depth - 1)})"
    op = kind
    return f"{_random_bool_query(rng, depth - 1)} {op} {_random_bool_query(rng, depth - 1)}"


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_or(impl):
    idx = impl.DocumentIndex()
    idx.insert_doc(1, ["a", "b", "c"])
    idx.insert_doc(2, ["b", "d"])
    idx.insert_doc(3, ["e"])
    assert idx.check_contains_or("a b c") == [1, 2]
    assert idx.check_contains_or("e") == [3]


@pytest.mark.part1
@pytest.mark.edge
def test_no_matches_returns_empty_list(impl):
    idx = impl.DocumentIndex()
    idx.insert_doc(1, ["a"])
    assert idx.check_contains_or("zzz") == []


@pytest.mark.part1
@pytest.mark.edge
def test_reinsert_replaces_document(impl):
    idx = impl.DocumentIndex()
    idx.insert_doc(1, ["a"])
    idx.insert_doc(1, ["b"])  # replaces -- doc1 should no longer match "a"
    assert idx.check_contains_or("a") == []
    assert idx.check_contains_or("b") == [1]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(150):
        idx = impl.DocumentIndex()
        docs = _random_docs(rng, rng.randint(1, 6))
        for doc_id, words in docs.items():
            idx.insert_doc(doc_id, sorted(words))
        query = " ".join(rng.sample(WORDS, rng.randint(1, 3)))
        assert idx.check_contains_or(query) == _brute_or_matches(query, docs), (docs, query)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_and_binds_tighter_than_or(impl):
    idx = impl.DocumentIndex()
    idx.insert_doc(1, ["a", "b"])
    idx.insert_doc(2, ["e"])
    idx.insert_doc(3, ["a"])  # has 'a' but not 'b' -- must NOT match "a AND b"
    # "a AND b OR e" == "(a AND b) OR e" -> doc1 (a&b), doc2 (e)
    assert idx.check_contains_bool("a AND b OR e") == [1, 2]


@pytest.mark.part2
@pytest.mark.edge
def test_not_and_parens_rejected_in_part2(impl):
    idx = impl.DocumentIndex()
    idx.insert_doc(1, ["a"])
    with pytest.raises(ValueError):
        idx.check_contains_bool("NOT a")
    with pytest.raises(ValueError):
        idx.check_contains_bool("(a OR b)")


@pytest.mark.part2
@pytest.mark.edge
def test_bool_against_brute_force_no_not_or_parens(impl):
    rng = random.Random(1)
    for _ in range(200):
        idx = impl.DocumentIndex()
        docs = _random_docs(rng, rng.randint(1, 6))
        for doc_id, words in docs.items():
            idx.insert_doc(doc_id, sorted(words))
        # build a query with only AND/OR (no NOT, no parens)
        parts = [rng.choice(WORDS)]
        for _ in range(rng.randint(0, 3)):
            parts += [rng.choice(["AND", "OR"]), rng.choice(WORDS)]
        query = " ".join(parts)
        assert idx.check_contains_bool(query) == _brute_matches(query, docs), (docs, query)


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_not_and_parens(impl):
    idx = impl.DocumentIndex()
    idx.insert_doc(1, ["a", "b"])
    idx.insert_doc(2, ["b"])
    idx.insert_doc(3, ["c"])
    assert idx.check_contains_full("NOT (a OR c)") == [2]


@pytest.mark.part3
def test_delete_doc_removes_from_index(impl):
    idx = impl.DocumentIndex()
    idx.insert_doc(1, ["a"])
    idx.insert_doc(2, ["a", "b"])
    idx.delete_doc(1)
    assert idx.check_contains_full("a") == [2]
    assert idx.check_contains_full("NOT a") == []


@pytest.mark.part3
@pytest.mark.edge
def test_delete_nonexistent_doc_is_a_noop(impl):
    idx = impl.DocumentIndex()
    idx.insert_doc(1, ["a"])
    idx.delete_doc(999)  # must not raise
    assert idx.check_contains_full("a") == [1]


@pytest.mark.part3
@pytest.mark.edge
def test_malformed_query_raises(impl):
    idx = impl.DocumentIndex()
    idx.insert_doc(1, ["a"])
    with pytest.raises(ValueError):
        idx.check_contains_full("(a OR b")  # missing ')'
    with pytest.raises(ValueError):
        idx.check_contains_full("a AND")  # dangling operator


@pytest.mark.part3
@pytest.mark.edge
def test_full_against_brute_force_random(impl):
    rng = random.Random(2)
    for _ in range(200):
        idx = impl.DocumentIndex()
        docs = _random_docs(rng, rng.randint(1, 6))
        for doc_id, words in docs.items():
            idx.insert_doc(doc_id, sorted(words))
        query = _random_bool_query(rng, depth=3)
        assert idx.check_contains_full(query) == _brute_matches(query, docs), (docs, query)


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part3
@pytest.mark.perf
def test_perf_many_docs_and_queries(run_script):
    rng = random.Random(0)
    lines = ["PART 3"]
    vocab = [f"w{i}" for i in range(50)]
    for doc_id in range(1, 50_001):
        words = rng.sample(vocab, 3)
        lines.append(f"INSERT_DOC {doc_id} {' '.join(words)}")
    for _ in range(2000):
        w1, w2 = rng.sample(vocab, 2)
        lines.append(f'CHECK_CONTAINS "{w1} OR {w2}"')
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 2000
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script('PART 1\nINSERT_DOC 1 a b c\nINSERT_DOC 2 b d\nCHECK_CONTAINS "a b c"\n')
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1 2\n"


@pytest.mark.part1
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part1_none(run_script):
    r = run_script('PART 1\nINSERT_DOC 1 a\nCHECK_CONTAINS "zzz"\n')
    assert r.returncode == 0, r.stderr
    assert r.stdout == "NONE\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script(
        'PART 2\nINSERT_DOC 1 a b\nINSERT_DOC 2 e\nINSERT_DOC 3 a\nCHECK_CONTAINS "a AND b OR e"\n'
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1 2\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    r = run_script(
        'PART 3\nINSERT_DOC 1 a b\nINSERT_DOC 2 b\nINSERT_DOC 3 c\n'
        'CHECK_CONTAINS "NOT (a OR c)"\nDELETE_DOC 1\nCHECK_CONTAINS "a"\n'
    )
    assert r.returncode == 0, r.stderr
    # first query: docs NOT containing a or c -> doc2 ({b}). After deleting doc1 ({a,b}), the
    # only doc that ever had 'a' is gone, so "a" matches nothing -> NONE.
    assert r.stdout == "2\nNONE\n"
