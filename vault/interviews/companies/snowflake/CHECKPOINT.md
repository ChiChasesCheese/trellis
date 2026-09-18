# Snowflake kit — 进度断点

> **唯一目的：让下一个会话在零上下文的情况下接着干。** 权威顺序：git 历史 > 本文件 > `LEDGER.md`。
> 分支 `worktree-snowflake-loop`。编排：主会话，子代理 `sonnet` 并行 ≤ 3，一任务一验收一 commit。方法论见 `.claude/skills/building-company-interview-kits/`。

## 一句话现状（2026-09-17）

Chakra 已面（16:34，Talent Intake 形式 14 问）；复盘在 `debrief/2026-09-17-chakra/REVIEW.md`：语法/填充词干净，掉分在无 headline、5 答 > 90 s、JD 关键词缺失、几处失言；下一场（recruiter call）前只练 headline-first 与证据词。工具链 `core/debrief/` 可复用于每一轮。
Chakra AI 轮一站式目录建成：`loop/rounds/00_ai_screen/`（playbook · stories S1–S10 · scenarios 12 · questions 71 题 + bank.json · rubric · CARD），`python3 loop/mock.py bq ai -n 5` 抽题；知识树 59 技能 92 题 strict 0/0。截止 2026-09-24。

## 上一版现状（2026-09-14）

题集建设完成：OA 23 · 电面 coding 28 · OOD 15（均 `verify_suites` 独立验收，66 题 1421 测试全绿）· 系统设计 21 · 非编码题库 74 题 · 题解文章 55 篇 · 知识树 59 技能 91 题 strict 0/0。
**覆盖率（`tools/coverage.py`，全集含 GitHub 蒸馏）= 175/178 = 98%**；未建 3 题各有原因（q11 无题面、q18 LOW、pc08 为 2019 三题组合且两题已由 q06/q07 覆盖）。LeetCode 公司标签 104 题见 `core/leetcode/companies/snowflake.md`。

## 阶段与状态

| 阶段 | 内容 | 状态 | 验收 |
|---|---|---|---|
| P0 | stripeoa 全量同步；kit 骨架；CLAUDE.md；settings | ✅ | 检查点 1 |
| P1 | 三路尽调 + 收割（raw 8 文件、discovery、TRIAGE 46 行） | ✅ | 检查点 2、7 |
| P2 | CATALOG（A–E）· RANK · PARETO（cut line 第 35 行）· LOOP_GUIDE · 知识树 · skills_matrix | ✅ | 检查点 2、7 |
| P3 | cut line 内全部建题（q11 仅标题不建）；非编码题库 | ✅ | `verify_suites` 27/27；检查点 3–13 |
| P4 | study 全部 + 题解 27 篇 | ✅ | 检查点 9、14 |
| P5 | TEST_SUMMARY · 00-README 重写 · coverage 工具 | ✅ | 本次提交 |
| P6 | 单来源题补齐：LC 原题组（56 · 1851 · 2002 · 261 · 1639 · 1962 · 253 · 2050 · 212 · 1600）+ 括号 · 服务启动 · 字符频次 · Top Two Users | ✅ | `coverage.py` 合计 ≥ 90%；`verify_suites` 全绿 |
| P6.5 | GitHub 优先蒸馏 → `catalog/raw/github_repos.md`；LC 通用题单；**P6.7 补建 26 个缺口 id**：pc16–pc29 · od11–od15 · q20–q25 · sd23（题面要点见 github_repos §3） | ✅ | 每批 `verify_suites` 全绿；`coverage.py` 分母加入 TrueInterview 清单后重算 |
| P7 | `/agent-skills:review` 评审（自包含 / 覆盖 / 教科书体例）→ 修正 → PR → merge main → `git pull` → `trellis` 同步 Obsidian 与 Anki | ⬜ | trellis validate 0 错；pytest 绿 |

## 已知的有意缺口

- **Chakra 题库（2026-09-17）**：`loop/rounds/00_ai_screen/` 按 senior 口径写，数字只留量级。四处说法用了"强势但可顶追问"的措辞，Chi 面前自己定性：① Ruby/Rails 旧路径 → 讲成"我的管线是接收侧的 Snowflake-native 替代"；② 商户级 quality-check → "designed, reviewed, proven for one subject area, sequenced behind the ramp"（ADR 仍 Proposed）；③ repo 份额 → "~90 PRs，两个最大改动是我的"（不说 #1 committer）；④ S9 出款事故 → 根因是本组 PR 的 effective-date 改动，我的贡献是 SLA 定论 + 主张 region conditional。`$138.6B` 疑为分/元口径差 100×（`core/stories/raw/HANDOFF-snowflake-queries.md` T2），口播稿已不依赖该数。
- `core/stories/raw/` 未被 gitignore（README 声称 `.gitignore:32`，实际无此规则）且仓库 PUBLIC —— 本次提交未 add 它；`core/tech_stacks/` 同样未提交。

- q11 Generating Login Codes：来源只有标题 + 标签，无题面，不建。
- sd13–sd20：仅聚合站题库标题（LOW），`catalog/raw/system_design.md` §3 第 5 条判定为聚合站自建题；按覆盖面在 P6 之后视剩余时间补 prompt 级简版。
- 子代理在 2026-09-13 撞过一次 sonnet 会话用量上限；中断点与抢救记录在 LEDGER。

## 下一步（接手就做这个）

1. P7 评审：自包含（每个题集只靠本目录 + 链接能做）、覆盖率口径诚实、全书是否像教科书（00-README 目录 → 轮次 → 题 → 题解）；修正后开 PR 合并。
2. 同步：`uv run trellis --all sync` → `build` → `anki-push`（需桌面 Anki）。公司 kit 不是 trellis domain，不产生卡片。
3. Snowflake 原理知识另起 trellis domain `snowflake`（skill `building-study-domains`，`vault/domains/snowflake/BUILD.md` 记进度），与本 kit 双向链接。
