# Headlands kit — 进度断点

> **唯一目的：让下一个会话在零上下文的情况下接着干。** 权威顺序：git 历史 > 本文件 > `LEDGER.md`。
> 分支 `headlands-kit`。编排：主会话，子代理 `sonnet` 并行 ≤ 3，一任务一验收一 commit。方法论 `.claude/skills/building-company-interview-kits/`，形状照抄 `companies/millennium/`。

## 一句话现状（2026-10-20，v2）

电面 **2026-10-26 12:00 PT**（Teams + CoderPad；C++ 或 Java 由面试官定；禁止 AI）。v2 按 Amazon kit 架构重建：
`behavioral/`（背景问题层）、`study/20-cpp/`（C++ 课本 16 课）、6 道题的 C++ 版（`tools/cpptest.py`）、`kq_cpp_depth/`（44 题 + 速查表）、
新 README / LOOP_GUIDE；全部学习文章按 CORE RULE（简洁、无出处、自包含）清理。规则在 `AGENT_RULES.md`。

验收（2026-10-20 全部通过）：`jtest.py verify` 15/15 · `cpptest.py verify` 6/6 · Java 21 示例 javac OK · C++ 课本 73/73 · 基础课本 44 代码块 · `mock_maven` mvn test OK。

## 下一步

1. Chi：README「面试前必须处理」三项；按 LOOP_GUIDE 的 6 天表练（关掉 AI）。
2. 可选：hc01/hc06/hc08/hc09/hc11/hc13 的 C++ 版；Amazon kit 按 CORE RULE 清理（等 Chi 说）。

## 阶段与状态

| 阶段 | 内容 | 状态 | 验收 |
|---|---|---|---|
| P0 | 骨架 + Java 21 工具链（`openjdk@21` brew、JUnit console jar 在 `~/.cache/trellis-java/`） | ✅ | `jtest.py verify` |
| P1 | 三路尽调 `catalog/raw/{github_repos,forums,official_and_process}.md` | ✅ | — |
| P2 | CATALOG（A–G）· RANK 43 行 · PARETO（cut line 第 22 行） | ✅ | `tools/pareto.py catalog/RANK.md --table 总表 --focus 电面` |
| P3 | `loop/LOOP_GUIDE.md`（视频面） | ✅ | — |
| P4 | 题集 + 讲义：oa01 hc01–hc09 hc11 hc13 ld01（13 个目录全部 verify OK） | ✅ | `python3 tools/jtest.py verify "loop/rounds/*/*"` |
| P5 | `study/10-java21/` J01–J19 · `study/00-foundations/` 6 章 | ✅ | 示例全部 javac 通过 |
| P6 | kq 语言深度题库 45 题 · 简报 · fit · stories（3 处待 Chi 填）· 反问 | ✅ | — |
| P7 | README 学习路径 ✅；onsite 层（senior 标准）：04_sd 设计轮指南 + sd01–sd03 + ld02 + ld03 ✅，38 处库/法规细节核对（31 对 7 改）；可选：hc10/hc12/hc15–hc20、oa02 | ✅（可选项待 Chi 决定） | — |

## 公开仓库约束

邮件里的姓名、邮箱、线程 ID、可用时段链接一律不进仓库；时间线只保留到「日期 + 阶段」。

## 下一步（接手就做这个）

1. Chi：签 NDA → 提交可用时段；按 `README.md` 学习路径刷；`stories.md` 的 3 个模板（性能排查、Quant-Stroller、code review）要 Chi 本人填。
2. Chi 若读到 1p3a 正文（1169914、1134455、1089956、1059121），把 (reconstructed) 的 Part 改成原题。
3. 过了电面：展开 onsite（`02_onsite/`、`04_sd/`），见 CATALOG C / LOOP_GUIDE §2。
4. 合并 PR #46 只在 Chi 说了之后。
