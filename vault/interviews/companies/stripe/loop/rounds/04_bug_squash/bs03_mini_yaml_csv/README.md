# miniyaml — a tiny indentation-sensitive YAML subset + CSV bridge

`miniyaml` is a small parser for a YAML subset (scalars, nested mappings, lists of scalars, and
lists of mappings written in the compact `- key: value` form), plus a converter between a
top-level "list of records" document and CSV text. It exists as a bug-squash fixture — the shape
(a lexer that turns lines into indent-tagged tokens, a recursive-descent parser that turns those
into nested Python data, and a schema-free CSV bridge) mirrors real parsers like `SnakeYAML`
closely enough that its actual historical bug shapes port over directly.

## Layout
```
src/miniyaml/
  lexer.py    tokenize(text): one Line per non-blank/non-comment source line, tagged with its
              indent and whether it's a map entry or a "- " list item (and which kind of item)
  scalars.py  coerce_scalar(raw): text -> int/float/bool/None/string; scalar_to_text(): the
              reverse mapping used when writing a CSV cell
  parser.py   Parser: recursive-descent-over-indentation parser (Parser().parse(text) or the
              parse_text(text) shortcut) that turns a Line stream into nested dict/list/scalar
  csvio.py    to_csv_text(records) / from_csv_text(text): a top-level list-of-mappings document
              to/from CSV, column set = every key seen across all records
tests/
  test_miniyaml.py   the suite (run it, don't rewrite it — see "if you're stuck" below)
```

## Running the tests
```
python -m pytest tests
```
Most tests pass as shipped. Two do not — see the issue below.

## The issue (as filed against this repo)

**Bug report 1 — a list item's second and later keys go missing (and so does everything after it)**

> Repro:
> ```python
> from miniyaml.parser import parse_text
>
> doc = "- name: Alice\n  age: 30\n  active: true\n- name: Bob\n  age: 25\n  active: false\n"
> parse_text(doc)
> ```
> Expected:
> ```python
> [{"name": "Alice", "age": 30, "active": True}, {"name": "Bob", "age": 25, "active": False}]
> ```
> Actual:
> ```python
> [{'name': 'Alice'}]
> ```
> `age` and `active` are gone from the first record, and the *entire second record* is gone too.
> A list item written as a single `- key: value` line with no continuation lines (e.g. `- id: 1`)
> parses fine. It's specifically a list item whose mapping has a *second* key, written on the
> line(s) below the dash, that breaks — and it doesn't just lose that one key, it seems to throw
> off everything the parser reads afterward.
>
> A plain nested mapping (no lists involved at all, however many levels deep) parses correctly at
> every depth we tried. This only reproduces once a list-of-mappings with multi-key items is
> involved.

**Bug report 2 — reusing one parser instance for a second document returns garbage**

> Repro:
> ```python
> from miniyaml.parser import Parser
>
> p = Parser()
> p.parse("a: 1\nb: 2\nc: 3\n")
> p.parse("x: 9\n")   # <- a brand new, unrelated document
> ```
> Expected: the second call returns `{"x": 9}` — a `.parse()` call shouldn't care what document
> the same `Parser` object was asked to parse before it.
>
> Actual: the second call returns `{}`. Calling `Parser().parse("x: 9\n")` with a **fresh**
> instance (never used for anything else) returns the correct `{"x": 9}` every time — it's
> specifically reusing the same `Parser` object for a second, unrelated `.parse()` call that
> breaks.

If you get stuck: both bugs are narrowly scoped (one wrong constant in an existing expression; one
missing reset of an existing field) — if your fix touches more than a handful of lines, or you
find yourself rewriting the recursive-descent structure or introducing a brand-new indent-tracking
scheme, you've drifted from the actual bug into a redesign. Come back to the failing assertion and
follow the traceback.
