---
nodes: [input.delimited, input.malformed, input.normalization, output.formatting, verification.edge-catalog, python.stdlib]
---
# Drill: parse, validate and report over a hostile CSV

Thirty-five minutes. Rows arrive on stdin with a fixed column order and an
optional header. Each row describes an onboarding record and must pass a growing
list of checks: every field non-empty after trimming; a descriptor whose length
falls inside an inclusive range; a descriptor that is not one of a set of generic
values compared case-insensitively with inner whitespace collapsed; and a URL
whose scheme and host satisfy stated rules. Print one line per row in input
order: `OK: <name>` or `FAIL: <name> (CODE, CODE)` with the codes in a fixed
order, and the name exactly as given after trimming.

**Constraints to state and honor**
- Quoted fields may contain the delimiter and must survive parsing.
- Missing trailing columns count as empty; extra columns are ignored.
- Every rule is evaluated, so one row can carry several codes.
- Up to 10^5 rows, 2 s, 256 MB.

**Grading points**
- `csv.reader` or `DictReader`, not `line.split(",")` — and say why out loud.
- One validator returning a list of codes, rather than `try`/`except` scattered
  through the parser.
- Normalization (trim, case-fold, collapse whitespace) happens once, at the
  boundary, and the *original* name is what gets printed.
- Header detection that cannot mistake a real row for a header.
- Empty input, a single row, a row of only delimiters, and a row whose name is
  itself a quoted string containing a comma
  ([[cc-verification-edge-empty-and-single]]).
- The order of the reason codes is part of the contract, not of the check order.

**Attempt log**
- [ ] Attempt 1 (date, 35 min, self-graded notes):
