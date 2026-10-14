# Headlands kit — 进度断点

> **唯一目的：让下一个会话在零上下文的情况下接着干。** 权威顺序：git 历史 > 本文件 > `LEDGER.md`。
> 分支 `headlands-kit`。编排：主会话，子代理 `sonnet` 并行 ≤ 3，一任务一验收一 commit。方法论 `.claude/skills/building-company-interview-kits/`，形状照抄 `companies/millennium/`。

## 一句话现状（2026-10-14）

Chi 投 Headlands Technologies **Software Engineer（Java）**，通过 HackerRank「Headlands Tech Coding Test - Java」，被邀约 **一小时技术视频面（phone screen）**；先签 NDA，再提交多个工作日可用时段。

## 阶段与状态

| 阶段 | 内容 | 状态 | 验收 |
|---|---|---|---|
| P0 | 骨架（tools/conftest/pytest.ini/check_tree.py 从 snowflake 复制） | ✅ | — |
| P1 | 三路尽调：A GitHub（`raw/github_repos.md`）· B 面经（`raw/forums.md`）· C 官方/JD/流程/薪资（`raw/official_and_process.md`） | 进行中（sonnet ×3） | 每个文件有来源表 + 缺口段 |
| P2 | CATALOG · RANK · PARETO · 简报 · 流程 · fit · 反问 | 待做 | `tools/pareto.py` |
| P3 | 技术视频面 playbook · 题库 | 待做 | — |
| P4 | 题集（cut line 以上） | 待做 | `tools/verify_suites.py` |
| P5 | 知识树 · CONTENTS · COVERAGE · README | 待做 | `check_tree.py --strict` |

## 公开仓库约束

邮件里的姓名、邮箱、线程 ID、可用时段链接一律不进仓库；时间线只保留到「日期 + 阶段」。

## 下一步（接手就做这个）

1. 等 P1 三个文件落地 → 主会话审（来源可达性、推断标注、HRT 混淆）→ commit。
2. P2：合并成 `catalog/CATALOG.md`，`tools/pareto.py` 出 cut line。
