# Agent rules — Headlands kit v2 (rebuilt on the Amazon kit's architecture)

Repo `/Users/chiserver/sessions/trellis`, branch `headlands-v2` (checked out; never switch branches). Kit root:
`vault/interviews/companies/headlands/`.

## Facts fixed by the orchestrator (first-hand, from Chi's email, 2026-10-16/19)

- Role: Software Engineer (Java), Headlands Technologies (Chicago). HackerRank Java test passed (job-chain problem).
- **Next round: technical video call, Mon 2026-10-26 12:00 PT, Microsoft Teams + CoderPad live coding.** Content:
  "technical and background questions, as well as live coding"; "most calls typically do not last the full hour".
- **"We do most of our work in C++, so if you need to do any brushing up then that might help. The language preference
  is often up to the discretion of the interviewer."** → prepare C++ to the same depth as Java.
- **No AI tools allowed in the interview** ("any instance where AI use is suspected will result in a rejection").
- The forum evidence (`catalog/raw/forums.md`, `catalog/CATALOG.md`) is almost all from C++ candidates: the language-depth
  questions ("why is C++ fast", "C++11/14/17/20 differences", "smart pointers", "malloc vs new", "std::copy vs memcpy",
  IPC/shared memory) now apply **as asked**, not only as Java translations.
- The repo is public: never write names, email content, meeting or CoderPad links.

## House rules (same as the Amazon kit)

- **Textbook mode** (`study/TEXTBOOK.md`): Chi says fundamentals are rusty — from zero, causes and effects, worked examples,
  self-checks with answers in `<details>`. Chinese with English terms in parentheses; anything Chi says aloud is English.
- **Senior bar, always** (Chi: 「不要调整 bar 我们永远准备的内容对标 senior」): senior follow-ups everywhere.
- **Stories** use `vault/interviews/core/stories/SPOKEN_FORMAT.md` (chronological S/T/A/R/L bullets, bold keywords, prose in
  `<details>`). Facts only from `core/stories/`, `core/resume/resume.tex` (corrected 2026-10-15: no "$600B", no
  "spearheaded net settlement"), `core/Answers.md`; missing facts are 【待 Chi 补：…】.
- Every number in prose comes from a run or a script; every external claim has a URL + date (`推断` for inference).
- C++: compile with `clang++ -std=c++20 -O2 -Wall -Wextra -fsanitize=address,undefined`; every snippet in a lesson must
  compile (keep runnable copies under an `examples/` dir and compile them all before replying).
- You own only the files named in your task. Do not commit, do not spawn agents. Subagent writes to files named
  `REPORT.md` are refused by the harness: put such content in your final reply.
- Final reply ≤ 12 lines: what you wrote (counts from a script), gate/compile results, weakest claims.
