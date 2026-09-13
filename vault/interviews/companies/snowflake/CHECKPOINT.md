# Snowflake kit — 进度断点

> **唯一目的：让下一个会话在零上下文的情况下接着干。** 权威顺序：git 历史 > 本文件 > `LEDGER.md` > `tasks/plan.md`。
> 分支 `worktree-snowflake-loop`（trellis 仓库）。编排：Fable 5.1 主会话，子代理一律 `sonnet`，并行 ≤ 3，每代理只写自己名下目录，一任务一验收一 commit。

## 一句话现状（2026-09-13）

Stripe 全量 kit（stripeoa `d36756f`）已同步进 `companies/stripe/`；Snowflake 目前只有 AI 轮材料（00–07 + CARD + fit + raw/）。**正在做：P1 尽调（三路 sonnet 并行，2026-09-13 启动）**。

## 阶段与状态

| 阶段 | 任务 | 状态 | 验收 |
|---|---|---|---|
| P0 | 同步 stripeoa 全量 → `companies/stripe/`；kit 自检 | ✅ | `pytest problems` 绿；文件数 ≥ 1000 |
| P0 | 复制 kit 骨架到 `companies/snowflake/`（drill.py, loop/mock.py, tools/, conftest.py, pytest.ini, CONVENTIONS.md） | ✅ | `python3 drill.py list` 可跑 |
| P1 | 尽调 A：OA + 电面 coding + OOD 题目（raw + 表） | ⬜ | `catalog/raw/coding_*.md` 每题带 URL/日期/置信度 |
| P1 | 尽调 B：system design + project deep dive + HM/BQ + team matching | ⬜ | `catalog/raw/sd_bq_*.md` |
| P1 | 尽调 C：1p3a 镜像（t.me/s/usinterview）+ Reddit RSS + HN 收割 | ⬜ | `catalog/discovery/` 有 json + 索引 |
| P2 | `catalog/CATALOG.md`（28 法则排序，写明 cut line）+ `LOOP_GUIDE.md` | ⬜ | 每行有 #refs/置信度；check 脚本 0 错 |
| P3 | OA 题库 `problems/qNN`（Top 20% 先做，带测试） | ⬜ | `pytest problems` 绿；`tools/summary.py` |
| P3 | 电面/onsite `loop/rounds/03_phone_coding`、`04_ood`（题 + 测试） | ⬜ | `loop/mock.py test` 绿 |
| P3 | `loop/rounds/05_system_design/sdNN`（prompt/rubric/model_answer/followups） | ⬜ | 每题 4 文件齐 |
| P3 | 非编码轮 `01_recruiter` `06_project_deep_dive` `07_hm_behavioral` `08_team_matching`（bank.json/questions/rubric/stories） | ⬜ | `mock.py bq` 可抽题 |
| P4 | `study/`（essentials + 每轮准备 + 每题文章，中文）+ `loop/tree/interview-loop.yaml` | ⬜ | `check_tree.py --strict` 0 错 |
| P5 | 验收：summary、README、00-README 更新、PR、merge | ⬜ | trellis validate 0 错 |

## 下一步（接手就做这个）

见 `tasks/plan.md` 里第一个未打勾的任务。
