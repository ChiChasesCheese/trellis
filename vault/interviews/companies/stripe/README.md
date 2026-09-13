# Stripe OA drill kit

Self-contained practice kit for Stripe's 60-minute, language-agnostic, multi-part HackerRank
challenge. Everything here is Python 3.11+ / pytest, no third-party deps.

```
catalog/            CATALOG.md — every Stripe OA/phone-screen problem found online, deduped,
                    with sources, confidence, frequency and variants
problems/qNN_slug/  problem.md · starter.py (yours) · solution.py (reference) · test_qNN.py · REPORT.md
study/              中文题解 + 通用精华（读完能独立做出来的验收路径）→ study/README.md
skills_matrix.md    test targets / knowledge / experience  ↔  problems  ↔  Stripe JD lines
reports/            OVERALL_REPORT.md (+ per-problem REPORT.md lives next to each problem)
drill.py            60-minute drill runner (+ `status`: cross-problem progress board)
progress.jsonl      append-only log, one line per `test` run — feeds `drill.py status`
                    (git-ignored: it is per-machine state, like .drill.json)
conftest.py         shared fixtures (`impl`, `run_script` with time+RSS measurement)
```

## Start here

- **`CLAUDE.md`** — 长期规矩：赛道（只做 SWE backend）· 记账纪律 · 目录地图 · 协作约定 · 已知的红
- **`HANDOFF.md`** — 当前断点：做到哪、下一步、站点可达性台账
- `study/README.md` — **中文**题解 53 篇 + 通用精华（解题框架 · 核心考点 · 语法速查 · 陷阱清单 · 算法模式 · 调试 · 沟通）
- `reports/OVERALL_REPORT.md` — what the OA is, drill order, quality gates, caveats
- `catalog/CATALOG.md` — every problem found online with #independent refs + source URLs (Tables A/B/C)
- `skills_matrix.md` — 25 bespoke + 16 algorithm test targets ↔ problems ↔ JD lines
- `reports/TEST_SUMMARY.md` — 53 problem sets · 965 tests (regenerate: `python tools/summary.py --run`)

Drill order (OA stage × recency × refs): q01 → q09 → q02 → q18 → q17 → q07 → q03 → q15 → q29 → q08, then q04 q13 q05 q06 q10; phone-screen set q22 q21 q19 q25 q32; algorithms qA01–qA13.

## Drill protocol (do this, in this order)

```bash
python drill.py list                # pick one
python drill.py start q01           # prints the WHOLE statement, resets starter.py, starts a 60-min timer
#   ... write your code in problems/q01_*/starter.py ...
python drill.py test q01 -k part1   # lock Part 1 before touching Part 2
python drill.py test q01            # full suite (edge + fmt + perf + io) against YOUR code
python drill.py time q01            # minutes left
python drill.py ref q01             # sanity: reference solution passes everything
python drill.py status              # progress board: which problems are green, best time, trend
python drill.py status --all        # ... including the ones you have never touched
```

Rules that mirror the real thing: no debugger (print to **stderr**), stdout must be exact,
read every part before writing a line of code, and keep the first 5 / last 5 minutes for
reading / boundary checks respectively. See `reports/OVERALL_REPORT.md` for the play-book.

## Running the whole kit

```bash
make test          # all reference solutions, all tests
make perf          # only perf tests (time + memory budgets)
make test-starter Q=q01
```
