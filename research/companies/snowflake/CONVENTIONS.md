# Conventions for every problem set in `problems/`

Layout (one directory per problem, `qNN_slug/`):

```
problems/q01_chat_billing/
  problem.md            standardized statement: context, input format, rules, Part 1..N,
                        worked examples, explicit edge-case list, variants seen in the wild,
                        sources + confidence, "what this tests"
  starter_template.py   the stub the candidate fills in (function signatures per part + main()
                        reading stdin). `drill.py start` copies it to starter.py
  starter.py            working copy for the candidate (git-ignored? no — committed as a copy
                        of the template so tests can be pointed at it)
  solution.py           reference solution, same public API as the starter, plus main()
  test_q01.py           pytest suite; uses the `impl` fixture from /conftest.py
  cases/                optional: NN_name.in / NN_name.out stdin/stdout pairs used by io tests
  REPORT.md             per-problem report (see below)
```

## Public API contract (starter and solution MUST match)

* One pure function per part, named `part1(...)`, `part2(...)`, … taking plain Python
  data (list[str] of raw input lines is the default) and returning plain data
  (list[str] of output lines is the default). Later parts may call earlier ones.
* `def main(stdin=sys.stdin, stdout=sys.stdout)` that reads the whole input, dispatches on the
  first line (`PART <n>` when the problem is multi-part) and prints. Never print debug output
  to stdout; use stderr.
* Money: integer minor units (cents) or `decimal.Decimal` with an explicit rounding mode.
  Never float-accumulate. State the rounding rule in a comment next to where it is applied.
* Sorting: state the full tie-break key. Output ordering must be deterministic.
* Parsing: strip whitespace, tolerate blank lines and trailing newline, tolerate optional
  spaces around separators when the problem says so.

## Tests (`test_qNN.py`)

Mark every test with exactly one of `part1..part5`, plus `edge`/`fmt`/`perf`/`io` where
applicable (markers are declared in `pytest.ini`). Required coverage:

1. every worked example in `problem.md` (verbatim)
2. per-part corner cases: empty input, single record, duplicates, out-of-order events, zero and
   negative amounts, exact-threshold boundaries (==, one below, one above), Unicode/whitespace
   noise if parsing, ties in sorting, rounding half cases (x.xx5), very large numbers
3. format: exact string output (`$0.00` style, two decimals, separators, trailing spaces)
4. `perf`: generate the largest plausible input (e.g. 10^5–10^6 records) with `random.Random(0)`
   and assert wall time < the stated budget (default 2 s) and peak RSS < 256 MB using the
   `run_script` fixture; keep the generated input in memory (don't write files)
5. `io`: run the module as a script with stdin from an example and assert exact stdout

Use `impl.partN(...)` so the same suite runs against `starter.py` via `IMPL=starter`.

## REPORT.md per problem

Sections: Summary (what/why Stripe asks this) · Sources & confidence · Part-by-part approach ·
Pitfalls that hidden tests target · Complexity + measured time/memory · Test inventory
(counts per marker) · Skills exercised (bullet list, matched to `skills_matrix.md` ids).
