# P2 task — CATALOG + RANK + PARETO (one agent)

Read first: `raw/AGENT_RULES.md` (rules 1–7 apply), then the three evidence files
`raw/github_repos.md`, `raw/forums.md`, `raw/official_and_process.md`, then the reference shape
`../../millennium/catalog/{CATALOG.md,RANK.md,PARETO.md}` and `../tools/pareto.py` (read its docstring and argparse).

Facts fixed by the orchestrator (first-hand, may be cited as source "Chi 亲历 2026-10"):
- Chi applied for Software Engineer (Java), took the HackerRank "Headlands Tech Coding Test - Java", and
  **it was the job-chain CSV problem**. This is the first report of the Java variant; it is one more
  independent source for that row and confirms Java and C++ candidates get the same OA.
- Next round: a one-hour technical video call with an engineer (the focus round, label it `电面`).

You own: `catalog/CATALOG.md`, `catalog/RANK.md`, `catalog/PARETO.md`. Nothing else.

1. `CATALOG.md`: one row per **problem family** (merge a FastPrep title with the forum family it
   matches — e.g. FastPrep "Queue Mean Queries" + "Queue Mean from Corrective Snapshots" + 1p3a 1169914
   are one family with parts). Columns: ID · 题（别名）· 阶段 · parts · 最近 · #refs · 置信度 · 来源 (raw file §row) .
   `#refs` = independent sources: FastPrep counts 1 total per family no matter how many titles; a 1p3a
   thread mirrored on Telegram counts 1; Blind/WSO/Glassdoor/1p3a are independent of each other.
   Separate tables: A coding (phone screen / OA / onsite), B low-level design, C system design,
   D knowledge questions (language depth: C++ reports become a Java-equivalent row, labelled `推断：Java 对应`;
   OS / concurrency / networking), E behavioural / process. QR-only items (gradient descent, Pearson, stats MCQ)
   go in a separate table F and are excluded from ranking unless also seen in a SWE report.
   IDs: `hc01…` coding in rank order of the phone-screen focus, `oa01` the job chain, `ld/sd/kq/bq` for the others.
2. `RANK.md`: section `## 总表` with columns `| ID | 题 | 轮次 | 最近 | #refs | 置信度 |` (all ranked rows A–E),
   轮次 ∈ {电面, OA, onsite, 非编码}.
3. Run `python3 tools/pareto.py catalog/RANK.md --table 总表 --focus 电面` from the kit root
   (`vault/interviews/companies/headlands`) and paste the output into `PARETO.md` with the exact command
   and date on top, then two lines in Chinese: the cut line and what it means. Never type a count by hand.
4. Final reply ≤ 15 lines: row counts per table (from a script), the cut line, the top 8 ids with names,
   and the merges you were least sure about.
