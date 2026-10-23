# loop/ 进度断点 — 2026-09-03（会话 3，**套件完成**）

> OA 之后整套面试流程的 mock 套件。分支 `worktree-stripe-loop`（已 push 到 origin），worktree `/Users/chizhang/Code/ITV/stripe-oa/.claude/worktrees/stripe-loop/`。
> **以 git + `loop/LEDGER.md`（账本）+ `loop/tasks/todo.md`（任务清单）为准**；本文件只是入口。

## 工作方式（用户约定，按时间最新为准）
- 编排/理解/抽查 = 主会话；**所有产出型子代理 = `sonnet`**；**并行 ≤ 3**；每代理只写自己名下目录；一题落盘一题；协调者验收 → commit → LEDGER。
  - 2026-09-03：用户曾单次指示「spawn more than three」，本会话一度并行 5 个；随后用户明确**恢复上限 3**。≤3 是默认值，只有用户当次明确要求才可突破。
- **每个 stage 结束**：commit → `git push` → `python3 loop/study/30-articles/sync_obsidian.py` → `python3 loop/study/30-articles/to_anki.py`（三条分开跑）。
- 材料中文；专有名词/代码英文；文章二八定律：方法论/下笔/建模/代码组织，不堆 corner case。
- 不动 `loop/study/00-prereq/exercises/ex02_structure.py`（用户在改）。
  - 2026-09-03 更新：原先还列了 `catalog/`、`problems/`、`catalog/CATALOG.md`，理由是「用户侧有未提交改动」。该前提本次会话已不成立（工作区干净），且本轮任务要求写这几处，故解除。**改动前仍应先 `git status` 确认工作区干净。**
- pytest 注意：pytest.ini 已带 `-q`，命令里**别再加 `-q`**（会吞掉汇总行）。

## 状态
- [x] Phase 0–2：raw 6/6 · CATALOG · LOOP_GUIDE · tree.yaml + check_tree · mock.py · 电面 ps01–08 · 题图 artifact（`loop/tree/map/`）
- [x] Phase 3 部分：mockserver · cd01–07 · int01–03 · bs01；**int04 半成品（缺 starter/test/REPORT）、bs02 未开始**
- [x] Phase R（review + 文章）：ps01–08 · cd01–07 · int01–03 · bs01 全部 review + 19 篇文章（`loop/study/30-articles/`）
- [x] R7 收口（2026-09-02）：`pytest loop --ignore=loop/rounds/04_bug_squash` 499 绿；`loop/lint.sh` 绿；文章同步 Obsidian `Inbox/Stripe Loop/`（索引 + `Claude 接力.md`）与 Anki `Stripe::Loop::*`；遗留：4 篇文章骨架 41–46 行略超 40
- [x] **2026-09-03 全部 BACKLOG 清空**：int04 收尾 · bs02–bs05 · sd01–sd06 · recruiter/hm/behavioral 题库(66 题) ·
  study/10-rounds 八章 · 20-cards 四份(224 张) · 30-articles 补 19 篇(共 38 篇 → 185 张 Anki 卡)
- [x] 同期新增：Table C 二轮排查（3 份报告）· 来源登记表 + 复验工具 · drill/mock 进度板 ·
  6 道复原/重建题(ps09–ps13, q41) · Bitfont 三版本(cd08–cd10) · S25 技能编号 · DEBUG_101 调试入门

## 当前状态（2026-09-03）

| 指标 | 值 |
|---|---|
| 可练题目 | **92**（53 problems + 39 loop rounds） |
| `check_tree.py` | **errors=0 warnings=0**（首次全通） |
| `pytest problems` | 1033 绿 / 1 红 |
| `pytest loop`（除 bug squash + prereq 练习） | 714 绿 / 1 红 |
| bug squash | 五题各"补丁前 2 红、打补丁后全绿" |

两条红都是 **perf 预算**，且**本轮开工前就红**：`q07::test_perf_100k`（单独跑也红，3.4s vs 2.0s 预算）与
`cd06::test_perf_1m_rows`（**单独跑是绿的**，只在全量并跑时被 CPU 争用挤超时）。预算按开发机定，
**没有放宽任何预算**去让容器看起来绿。
`loop/study/00-prereq/exercises/test_ex02.py` 的 3 红是**用户自己的作答文件**（满篇 `# TODO`），红是正常状态。

## 下一会话怎么接
1. `git status` 盘点未提交目录（代理被 session limit 杀掉会留半成品）：跑 `rtk proxy python3 -m pytest <dir> --tb=no` + `loop/lint.sh <dir>`，绿的 commit。
2. 按 `loop/tasks/todo.md` Phase R 未勾选项发 sonnet 代理（任务书模板：读 checklist + CONVENTIONS + lint.sh + 文章模板 + 范文 ps01 → review → 修 → lint → 文章 → REPORT 追加 Review 节 → 返回 LEDGER 行）。
3. 每收一份：验收 → commit → LEDGER；stage 结束跑三连（push / obsidian / anki）。
4. 配额将近：先更新本文件 + LEDGER 并 commit + push，再停。
