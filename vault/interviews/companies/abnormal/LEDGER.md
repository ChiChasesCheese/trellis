# Abnormal kit — 账本（每个被接受的任务一行）

| 日期 | 任务 | 交付 | 验收命令 / 结果 | commit |
|---|---|---|---|---|
| 2026-10-06 | P0 骨架 | tools/ conftest pytest.ini check_tree mock.py（自 millennium）· `loop/ai_screen.py` · `CONVENTIONS.md`（codebase 题型）· `tools/verify_suites.py`（支持 acceptance/） | `python3 loop/ai_screen.py list` | — |
| 2026-10-06 | 一手材料 | `catalog/raw/inbox.md`（门户 AI Technical Screen 官方原文） | — | — |
| 2026-10-06 | 尽调 A/B | `catalog/raw/{process_and_rounds,questions_reported,github_repos,official,ai_screen_format}.md` | 编排者经 GraphQL 重取 #8335187、#8496901 原文逐字核对 | — |
| 2026-10-06 | CATALOG/RANK/PARETO · LOOP_GUIDE · playbook · 简报/流程/fit/反问 · 题库 hm 16 / team 10 · sd01 · study | — | `tools/pareto.py`：12 行，cut line 第 6 行 | — |
| 2026-10-06 | cb02_insiderwatch（sonnet） | 代码库 + 3 ticket + 31 验收测试 + interviewer/walkthrough；REPORT 由编排者保存 | `verify_suites.py`：OK（31 passed · starter core 19 failed · 53/71 own） | 见下一次提交 |
| 2026-10-06 | cb01_sentinel（sonnet） | 报道原形态代码库 + 3 ticket + 32 验收；编排者把 t3 `event_count` 放宽为 {9, 12}（两种口径都说得通）并在 interviewer.md 注明 | `verify_suites.py`：OK（32 passed · starter core 20 failed · 44/59 own） | 见提交 |
| 2026-10-06 | cb03_vetting（sonnet） | 团队领域代码库 + 3 ticket + 34 验收；REPORT 由编排者保存 | `verify_suites.py`：OK（34 passed · starter core 18 failed · 52/64 own） | 见提交 |
| 2026-10-06 | sd02 worker/queue scaling（编排者） | prompt/rubric/model_answer/followups，数字 `python3 -c` 计算 | — | 见提交 |
| 2026-10-06 | pc01_image_dedup（sonnet） | 4 parts（3–4 reconstructed）+ 34 tests + 题解 | `verify_suites.py`：OK（33 passed 1 skipped · starter 27 failed） | 见提交 |
| 2026-10-07 | cr01_alert_fanout + cr02_risk_api（sonnet，第二个因用量上限中断） | PR + diff + 隐藏测试 + REVIEW_KEY（各 13 条）+ walkthrough + followups；cr02 REPORT 由编排者补写 | `verify_suites.py`：cr01 OK（24 · core 8 红）· cr02 OK（24 · core 9 红） | 见提交 |
| 2026-10-07 | ic01（sonnet 中断，部分）→ ic01 补完 + ic02 交给 opus（恢复规则） | — | 待验收 | — |
| 2026-10-07 | ic01_ingest_lag + ic02_api_5xx（opus，恢复规则续做 ic01） | 离线 AWS 快照 + awsim.py + investigation/model_answer/rubric；model_answer 的每个证据块由测试重跑；REPORT 由编排者保存 | 编排者重跑：`pytest loop/rounds/02_incident_sd` → 152 passed | 见提交 |
| 2026-10-07 | 收尾 | `reports/COVERAGE.md`（26/31 = 84%）· `study/20-cards/aws_incident.md` · CONTENTS 10 题 · `check_tree.py --strict` 0/0 | — | 见提交 |
| 2026-10-07 | 尽调 sweep（sonnet） | `catalog/raw/ai_round_sweep_2026-10-07.md`：6 个新来源 + 题型地图 16 行；File Vault take-home 由编排者 `gh api` 复核 | — | 见提交 |
| 2026-10-07 | cb04_quarantine（sonnet；REPORT 由编排者代存） | fix-the-codebase：6 处埋点 + production-ready + burst；walkthrough 按 T 编号 | 编排者重跑 3 次：验收 38 passed · starter core 19 failed · starter 54 · solution 78 | 见提交 |
| 2026-10-07 | cb05_rulelang（sonnet；REPORT 由编排者代存） | 解析器 / Kahn 拓扑 / 带时间约束的 BFS | 编排者重跑：验收 36 passed · starter core 22 failed · starter 39 · solution 69 | 见提交 |
