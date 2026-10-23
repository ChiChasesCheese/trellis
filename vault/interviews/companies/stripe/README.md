# Stripe OA drill kit

Self-contained practice kit for Stripe's 60-minute, language-agnostic, multi-part HackerRank
challenge. Everything here is Python 3.11+ / pytest, no third-party deps.

```
problems/qNN_slug/  problem.md · starter.py (yours) · solution.py (reference) · test_qNN.py · REPORT.md
study/              中文题解 + 通用精华（读完能独立做出来的验收路径）→ study/README.md
loop/               OA 之后各轮（电面 · bug squash · integration · coding · 系统设计 · behavioral）→ loop/README.md
drill.py            60-minute drill runner (+ `status`: cross-problem progress board)
progress.jsonl      append-only log, one line per `test` run — feeds `drill.py status`
                    (git-ignored: it is per-machine state, like .drill.json)
conftest.py         shared fixtures (`impl`, `run_script` with time+RSS measurement)
```

## Start here

- `study/README.md` — **中文**题解 53 篇 + 通用精华（解题框架 · 核心考点 · 语法速查 · 陷阱清单 · 算法模式 · 调试 · 沟通）

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
reading / boundary checks respectively.

## Running the whole kit

```bash
make test          # all reference solutions, all tests
make perf          # only perf tests (time + memory budgets)
make test-starter Q=q01
```
