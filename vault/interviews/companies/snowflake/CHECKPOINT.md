# Snowflake kit — 进度断点

> **唯一目的：让下一个会话在零上下文的情况下接着干。** 权威顺序：git 历史 > 本文件 > `LEDGER.md` > `tasks/plan.md`。
> 分支 `worktree-snowflake-loop`（trellis 仓库，worktree `.claude/worktrees/snowflake-loop`）。编排：主会话（Fable 5.1 → 用量上限后 Opus 5），子代理一律 `sonnet`、并行 ≤ 3、每代理只写自己名下目录、一任务一验收一 commit。

## 一句话现状（2026-09-13）

全轮次 kit 已建成并逐批验收入库：OA 11 · 电面 coding 7 · OOD 9 · 系统设计 13 · 非编码题库 74 题 · 学习面（前置 4 · 精华 5 · 每轮 9 · 卡片 3 · 题解 27）· 557 测试全绿 · `check_tree --strict` 0/0。**覆盖率（`tools/coverage.py`）= 流出次数 98/124 = 79%，题族 40/66。** 正在做：**P6 补齐单来源题到 ≥ 90%**，然后评审、合并、同步。

## 阶段与状态

| 阶段 | 内容 | 状态 | 验收 |
|---|---|---|---|
| P0 | stripeoa 全量同步；kit 骨架；CLAUDE.md；settings | ✅ | 检查点 1 |
| P1 | 三路尽调 + 收割（raw 8 文件、discovery、TRIAGE 46 行） | ✅ | 检查点 2、7 |
| P2 | CATALOG（A–E）· RANK · PARETO（cut line 第 35 行）· LOOP_GUIDE · 知识树 · skills_matrix | ✅ | 检查点 2、7 |
| P3 | cut line 内全部建题（q11 仅标题不建）；非编码题库 | ✅ | `verify_suites` 27/27；检查点 3–13 |
| P4 | study 全部 + 题解 27 篇 | ✅ | 检查点 9、14 |
| P5 | TEST_SUMMARY · 00-README 重写 · coverage 工具 | ✅ | 本次提交 |
| **P6** | 单来源题补齐：LC 原题组（56 · 1851 · 2002 · 261 · 1639 · 1962 · 253 · 2050 · 212 · 1600）+ 括号 · 服务启动 · 字符频次 · Top Two Users | ⏳ | `coverage.py` 合计 ≥ 90%；`verify_suites` 全绿 |
| **P6.5** | GitHub 优先蒸馏 → `catalog/raw/github_repos.md`；LC 通用题单；**P6.7 补建 26 个缺口 id**：pc16–pc29 · od11–od15 · q20–q25 · sd23（题面要点见 github_repos §3） | ⏳ | 每批 `verify_suites` 全绿；`coverage.py` 分母加入 TrueInterview 清单后重算 |
| P7 | `/agent-skills:review` 评审（自包含 / 覆盖 / 教科书体例）→ 修正 → PR → merge main → `git pull` → `trellis` 同步 Obsidian 与 Anki | ⬜ | trellis validate 0 错；pytest 绿 |

## 已知的有意缺口

- q11 Generating Login Codes：来源只有标题 + 标签，无题面，不建。
- sd13–sd20：仅聚合站题库标题（LOW），`catalog/raw/system_design.md` §3 第 5 条判定为聚合站自建题；按覆盖面在 P6 之后视剩余时间补 prompt 级简版。
- 子代理在 2026-09-13 撞过一次 sonnet 会话用量上限；中断点与抢救记录在 LEDGER。

## 下一步（接手就做这个）

1. 收 P6 三个 sonnet（q12–q17 / pc07–pc15 / od07+sd13–16）→ 独立 `verify_suites` → LEDGER → commit。
2. 自写 sd18–sd20。
3. 派 P6.7 三批 sonnet 建 26 个缺口 id（按 `catalog/raw/github_repos.md` §3），同法验收。
4. `coverage.py` 把 TrueInterview 清单并入分母，重算后再写评审结论。
5. skill 已入库 `.claude/skills/building-company-interview-kits/`（未测试），跑基线 + 对照后修订。

旧说明：

跑 `python3 tools/coverage.py` 看"未建"列表，从出现次数最高、有题面的开始建；每建完一批跑 `python3 tools/verify_suites.py . "<glob>"`，记 LEDGER，commit + push。
