# loop/ 进度断点 — 2026-09-02（会话 2，review 阶段）

> OA 之后整套面试流程的 mock 套件。分支 `worktree-stripe-loop`（已 push 到 origin），worktree `/Users/chizhang/Code/ITV/stripe-oa/.claude/worktrees/stripe-loop/`。
> **以 git + `loop/LEDGER.md`（账本）+ `loop/tasks/todo.md`（任务清单）为准**；本文件只是入口。

## 工作方式（用户约定，按时间最新为准）
- 编排/理解/抽查 = 主会话 Fable 5.1；**所有产出型子代理 = `sonnet`**；**并行 ≤ 3**；每代理只写自己名下目录；一题落盘一题；协调者验收 → commit → LEDGER。
- **每个 stage 结束**：commit → `git push` → `python3 loop/study/30-articles/sync_obsidian.py` → `python3 loop/study/30-articles/to_anki.py`（三条分开跑）。
- 材料中文；专有名词/代码英文；文章二八定律：方法论/下笔/建模/代码组织，不堆 corner case。
- 不动 `catalog/`、`problems/`、`loop/study/00-prereq/exercises/ex02_structure.py`（用户在改）、`catalog/CATALOG.md`（用户侧未提交改动）。
- pytest 注意：pytest.ini 已带 `-q`，命令里**别再加 `-q`**（会吞掉汇总行）。

## 状态
- [x] Phase 0–2：raw 6/6 · CATALOG · LOOP_GUIDE · tree.yaml + check_tree · mock.py · 电面 ps01–08 · 题图 artifact（`loop/tree/map/`）
- [x] Phase 3 部分：mockserver · cd01–07 · int01–03 · bs01；**int04 半成品（缺 starter/test/REPORT）、bs02 未开始**
- [x] Phase R（review + 文章）：ps01–08 · cd01–07 · int01–03 · bs01 全部 review + 19 篇文章（`loop/study/30-articles/`）
- [x] R7 收口（2026-09-02）：`pytest loop --ignore=loop/rounds/04_bug_squash` 499 绿；`loop/lint.sh` 绿；文章同步 Obsidian `Inbox/Stripe Loop/`（索引 + `Claude 接力.md`）与 Anki `Stripe::Loop::*`；遗留：4 篇文章骨架 41–46 行略超 40
- ⏸ BACKLOG（用户指示暂停）：int04 收尾 · bs02–05 · sd01–06 · rc/hm/bq · study/10-rounds · 20-cards · TREE.md · README/INDEX

## 下一会话怎么接
1. `git status` 盘点未提交目录（代理被 session limit 杀掉会留半成品）：跑 `rtk proxy python3 -m pytest <dir> --tb=no` + `loop/lint.sh <dir>`，绿的 commit。
2. 按 `loop/tasks/todo.md` Phase R 未勾选项发 sonnet 代理（任务书模板：读 checklist + CONVENTIONS + lint.sh + 文章模板 + 范文 ps01 → review → 修 → lint → 文章 → REPORT 追加 Review 节 → 返回 LEDGER 行）。
3. 每收一份：验收 → commit → LEDGER；stage 结束跑三连（push / obsidian / anki）。
4. 配额将近：先更新本文件 + LEDGER 并 commit + push，再停。
