# Task — new Headlands practice problem(s), Java + C++, group {GROUP}

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never switch branches, never spawn agents. Kit:
`vault/interviews/companies/headlands/` (run its tools from that directory). Chi will write **every** kit problem twice
tomorrow (Java, then C++), so a new problem must be complete in both languages.

You own only: {OWN}

## Read first
- `research/companies/headlands/CONVENTIONS.md` (Java layout) and `vault/interviews/companies/headlands/CPP_CONVENTIONS.md`
  (C++ layout, `tools/cpp/minitest.hpp`).
- The template problem, copy its shape exactly: `loop/rounds/01_video/hc05_market_order_book/` — `problem.md`
  (opening paragraph, 读题前你需要知道, 背景, Part 一览 table, one section per Part with exact semantics and error rules,
  examples), `starter/` + `reference/` + `test/` (JUnit 5, tags `part1`… and `perf`), `cpp/{starter.hpp, reference.hpp,
  test.cpp}` with the same tests; study articles `study/30-articles/hc05_market_order_book.md` and `_cpp.md`.
- `proposals/WRITING_RULES.md` (learning pages: no provenance, Chinese, English terms, phone-safe diagrams).

## The problem(s)
{SPEC}

Design 3–4 Parts that grow like a real 45-minute interview: a clean core, then the follow-ups interviewers add
(streaming input, a window, edge cases and errors, a performance constraint). Prices are integer ticks or fixed-point
`long`, never floating point for money; state overflow rules. Same semantics and test cases in Java and C++.

## Acceptance (run yourself before replying)
- `python3 tools/jtest.py verify "loop/rounds/01_video/<id>"` — reference all green, starter compiles and at least one test red.
- `python3 tools/cpptest.py verify "loop/rounds/01_video/<id>"` — same for C++ (`-Werror`, sanitizers).
- `uv run python scripts/plain_style.py` (from repo root) on `problem.md` and both study articles; `scripts/phone_diagrams.py` ok.
- Do not touch any other problem, the kit README, or LOOP_GUIDE.

Reply ≤ 8 lines: files, verify results (test counts), and anything you are unsure about.
