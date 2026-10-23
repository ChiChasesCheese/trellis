# Implementation brief (read fully before writing anything)

Repo: /Users/chizhang/Code/ITV/stripe-oa  (Python 3.11, pytest, no third-party deps)

Read first, in order:
1. CONVENTIONS.md — file layout + API contract + test requirements + REPORT.md sections
2. problems/q03_chat_billing/ — the EXEMPLAR: copy its structure exactly
   (problem.md, starter_template.py, starter.py = copy of template, solution.py, test_qNN.py, REPORT.md)
3. catalog/raw/cn_sources.md and catalog/raw/process_and_jd.md — the research; every problem you
   implement has a section there with the reported rules, variants, sources and confidence.

Rules of engagement
- Work ONE problem at a time, in this order, writing each file to disk immediately:
  problem.md → starter_template.py (+ cp to starter.py) → solution.py → test_qNN.py → run tests → REPORT.md.
  Partial progress must be usable if you get cut off. Never batch several problems in your head.
- Run tests with:  rtk proxy python3 -m pytest problems/<dir> -q
  (plain `pytest` output is swallowed by a shell hook; `rtk proxy` shows it). Also run once with
  IMPL=starter to confirm the empty starter FAILS (proves tests are not vacuous).
- Do NOT git commit / git add — the coordinator commits.
- problem.md must contain: header line `# qNN · Title` + Type/Stage/Last asked/Frequency (# of
  independent sources)/Confidence, Context (1 paragraph of Stripe domain framing), Input format,
  Output format, Rules per Part (1..N — all parts the sources report; if a source only lists
  a part's title, design a faithful rule and mark it "(reconstructed)"), 3+ worked examples with
  hand-verified outputs, "Edge cases hidden tests are known to target", "Variants seen in the
  wild", "What this tests" (skill ids S01..S24 from process_and_jd.md section E numbering),
  Sources (URLs from the research files — copy them verbatim; do not invent URLs).
- When sources conflict, pick the version with the most independent sources as the primary and
  list the other under Variants; if a variant is cheap to support, expose it as a keyword flag on
  the solution function and test it too.
- Multi-part stdin protocol: if the parts share one program (rules accumulate), main() just reads
  lines. If parts have different commands/inputs, first stdin line is `PART n`. State it in problem.md.
- Tests: ≥ 15 per problem, every part covered, every worked example verbatim, boundary (==, one
  below, one above), duplicates/out-of-order/empty/single/zero/negative, exact formatting,
  one `io` test via run_script, one `perf` test (largest plausible input; < 2 s and < 256 MB
  unless the problem says otherwise). Use the `impl` fixture (see conftest.py) so IMPL=starter works.
- Solutions: correct first, then clean. Integer minor units for money. Deterministic tie-breaks.
  Comment the exact rule next to where it is applied (strict vs non-strict, rounding mode).
  Keep the solution the size a candidate could write in ~35 minutes (typically 60–150 lines).
- REPORT.md: sections exactly as CONVENTIONS.md lists, plus a line "Measured: <perf test seconds>s, <MB> MB".
- Finish by replying with: per problem — dir name, test counts (pass/fail), perf numbers, any rule
  you had to reconstruct or any conflict you resolved. Keep the reply under 300 words.
