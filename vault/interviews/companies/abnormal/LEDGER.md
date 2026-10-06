# Abnormal kit — 账本（每个被接受的任务一行）

| 日期 | 任务 | 交付 | 验收命令 / 结果 | commit |
|---|---|---|---|---|
| 2026-10-06 | P0 骨架 | tools/ conftest pytest.ini check_tree mock.py（自 millennium）· `loop/ai_screen.py` · `CONVENTIONS.md`（codebase 题型）· `tools/verify_suites.py`（支持 acceptance/） | `python3 loop/ai_screen.py list` | — |
| 2026-10-06 | 一手材料 | `catalog/raw/inbox.md`（门户 AI Technical Screen 官方原文） | — | — |
| 2026-10-06 | 尽调 A/B | `catalog/raw/{process_and_rounds,questions_reported,github_repos,official,ai_screen_format}.md` | 编排者经 GraphQL 重取 #8335187、#8496901 原文逐字核对 | — |
| 2026-10-06 | CATALOG/RANK/PARETO · LOOP_GUIDE · playbook · 简报/流程/fit/反问 · 题库 hm 16 / team 10 · sd01 · study | — | `tools/pareto.py`：12 行，cut line 第 6 行 | — |
| 2026-10-06 | cb02_insiderwatch（sonnet） | 代码库 + 3 ticket + 31 验收测试 + interviewer/walkthrough；REPORT 由编排者保存 | `verify_suites.py`：OK（31 passed · starter core 19 failed · 53/71 own） | 见下一次提交 |
