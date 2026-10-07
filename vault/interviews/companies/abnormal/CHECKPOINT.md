# Abnormal AI kit — 进度断点

> 唯一目的：下一个会话零上下文接着干。权威顺序：git 历史 > 本文件 > `LEDGER.md`。
> 分支 `claude/abnormal-ai-kit`。编排：主会话；子代理 `sonnet`，并行 ≤ 3，一任务一验收一 commit。方法论 `.claude/skills/building-company-interview-kits/`。

## 现状（2026-10-06）

Chi 已过 HR + HM（SWE II – Insider Risk）。下一轮 = **AI Technical Screen**（60 min，已有 Python 代码库 + Claude Code，探索 10 / 模糊 feature 35 / walkthrough 15），排期中。之后几轮未知。

## 阶段

| 阶段 | 内容 | 状态 |
|---|---|---|
| P0 | 骨架 + codebase 题型约定 + 练习 runner | ✅ |
| P1 | 尽调：A 面经/流程/GitHub · B 官方/产品/JD/AI 面试口径 | ✅ |
| P2 | 练习代码库 cb01 sentinel · cb02 insiderwatch · cb03 vetting（`tasks/AGENT_CODEBASES.md`） | ✅ 三个均过 gate |
| P3 | CATALOG / RANK / PARETO · LOOP_GUIDE · AI screen playbook · 其它轮（sd01 sd02 cr01 cr02 pc01 ✅；ic01/ic02 opus 进行中） | 大部分 ✅ |
| P4 | study（中文）· 知识树 · CONTENTS · COVERAGE · README | ✅（ic 完成后重跑 contents/coverage/check_tree --strict） |
| P5 | commit + push + draft PR | PR #43（draft） |

## 下一步

见上表第一个非 ✅ 行。子代理任务的恢复规则写在各自的 tasks/*.md 里。
