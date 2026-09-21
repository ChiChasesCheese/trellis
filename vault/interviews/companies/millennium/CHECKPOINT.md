# Millennium kit — 进度断点

> **唯一目的：让下一个会话在零上下文的情况下接着干。** 权威顺序：git 历史 > 本文件 > `LEDGER.md`。
> 分支 `claude/millennium-investigation-aouciq`。编排：主会话，子代理 `sonnet` 并行 ≤ 3，一任务一验收一 commit。方法论 `.claude/skills/building-company-interview-kits/`。

## 一句话现状（2026-09-21）

Chi 收到 **Millennium LEaD Program（Miami，REQ-27753）第一轮邀约：45 min · SWE 面试官 · Webex + HackerRank live coding**；其它 Millennium req 已被简历筛拒。kit 建成：证据 7 文件 · CATALOG 15 行（cut line 第 9 行）· R1 playbook · 题库 4 个（40/8/14/12）· 题集 pc01–pc10（子代理，各自 `verify_suites` 验收）· sd01 · 题解 10 篇 · 速记卡 2 · 知识树 6 轮 14 技能 0/0。

## 阶段与状态

| 阶段 | 内容 | 状态 | 验收 |
|---|---|---|---|
| P0 | 骨架（tools/conftest/pytest.ini/mock.py/check_tree.py 从 snowflake 复制并改轮次名） | ✅ | `mock.py bq py` 可抽题 |
| P1 | 三路尽调：邮件 · GitHub 优先 · 官方/JD · 面经（LC Discuss 全文、1p3a 镜像、Blind/Glassdoor 摘要、聚合站） | ✅ | `catalog/raw/sources_index.md` 每条可达性 |
| P2 | CATALOG（A–E）· RANK · PARETO · 简报 · 流程 · fit · 反问 · 回信草稿 | ✅ | `tools/pareto.py` |
| P3 | R1 playbook · 题库（py 40 · rc 8 · exp 14 · hm 12）· 速记卡 | ✅ | bank.json 生成自 questions.md |
| P4 | 题集 pc01–pc10（sonnet ×5 波）· sd01 | ✅ 10/10 ALL ACCEPTED · sd01 四文件 | `tools/verify_suites.py . "loop/rounds/01_first_round/pc*"` |
| P5 | 知识树 · CONTENTS · COVERAGE · README | ✅ | `check_tree.py --strict` 0/0 |
| P6 | 提交 + 合并 main | 去掉所有来自邮箱的标识（姓名、邮箱、线程 ID、时间线）后 push 通过；PR #38 已合并到 main（`e8b38027`） | 工作机 `bash scripts/sync_laptop.sh` 后 `verify_suites` 全 OK |

## 已知的有意缺口

- LEaD 自身题目零一手；Blind/Glassdoor/1p3a 正文未读（反爬）。**Chi 手动读**：1p3a thread-951597（2023 SDE intern timeline，NYC/Miami）、1124751、1158922；Blind "Millenium LEaD program"（j0mxzge4）。
- pc11 Merge Intervals、pc12 simple graph 未建（LC 原题 / 复用 Snowflake pc02/pc04）。
- 面试官信息只保留邀约中的姓名与公开头衔（仓库公开）。
- `mock.py status` 依赖 `tools/progress.py` 的 `problems/` 目录假设；本 kit 没有 OA 题（`problems/` 不存在），`status` 只显示 loop 题。

## 下一步（接手就做这个）

1. Chi：工作机 `git pull` main 后 `bash scripts/sync_laptop.sh`，然后 `cd vault/interviews/companies/millennium && python3 tools/verify_suites.py . "loop/rounds/01_first_round/pc*"` 确认 10 题全 OK。
2. Chi：回复邀约（`03-reply-email.md`），按 `loop/LOOP_GUIDE.md` §6 三天冲刺；面完填 `02-process.md` 亲历表并回写。
3. 若 recruiter 回信给出后续轮次结构 → 更新 `02-process.md` §2 与 `loop/LOOP_GUIDE.md`。
