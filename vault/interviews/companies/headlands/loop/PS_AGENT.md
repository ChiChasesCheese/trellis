# Problem-set agent instructions (Headlands, Java 21)

Repo `/Users/chiserver/sessions/trellis`, kit `vault/interviews/companies/headlands` (run every command from the kit root).

Read before writing anything:
1. `CONVENTIONS.md` — layout, API contract, test tags, the J01–J19 feature matrix, REPORT sections.
2. The pilot `loop/rounds/00_oa/oa01_job_chain/` — copy its shape exactly (problem.md, REPORT.md, starter/, reference/, test/).
3. Your rows in `catalog/CATALOG.md` and the evidence rows they cite in `catalog/raw/*.md`.

Rules:
- You own only the directories named in your task. Never edit CONVENTIONS, tools, catalog, other problems. Do not commit. Do not spawn agents.
- Resume rule: if a directory exists, read it, run the gate, and finish only what is missing.
- Learner-facing text (problem.md, REPORT.md, comments in starter) is **Chinese**, technical terms in English. Code identifiers English.
- Every part not in the evidence is labelled **(reconstructed)**; the evidence only gives a title + first sentence for most FastPrep items, so say which parts you invented.
- Each problem has 2–4 Parts that escalate the way a one-hour call with an engineer does: a clean base, then follow-ups
  on performance (complexity, allocation, cache locality), robustness (overflow, malformed input) and, where natural, concurrency.
- Use **≥ 4** Java 21 features from the matrix per problem, chosen because they fit (records/sealed/pattern switch for data,
  Sequenced Collections for ordered ends, virtual threads / StructuredTaskScope / VarHandle for concurrency parts, FFM `Arena` for memory pools).
  Prefer features not already used by the pilot when the fit is equal, so the kit covers the whole matrix.
- Tests: JUnit 5, tags per CONVENTIONS, include `perf` (seeded `Random(0)`, `assertTimeoutPreemptively`) and `conc` for any concurrent part
  (`CountDownLatch` start gate, repeat ≥ 20 rounds, assert invariants; no sleeps for ordering).
- Starter: same public API, records/sealed types given, method bodies `throw new UnsupportedOperationException("TODO")`; must compile.
- REPORT.md: all sections in CONVENTIONS, including ≥ 3 interviewer follow-ups with answer points; the test count comes from running the suite, not counting by hand.
- Measured times in REPORT come from an actual run on this machine.

Acceptance (run it yourself before replying; the orchestrator re-runs it):
`python3 tools/jtest.py verify "loop/rounds/*/<your-id>*"` → every line `OK`.

Final reply ≤ 12 lines: per problem — parts, test count, gate result, Java features used (ids), what is (reconstructed), weakest point.
