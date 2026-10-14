# Headlands kit — 进度断点

> **唯一目的：让下一个会话在零上下文的情况下接着干。** 权威顺序：git 历史 > 本文件 > `LEDGER.md`。
> 分支 `headlands-kit`。编排：主会话，子代理 `sonnet` 并行 ≤ 3，一任务一验收一 commit。方法论 `.claude/skills/building-company-interview-kits/`，形状照抄 `companies/millennium/`。

## 一句话现状（2026-10-14）

Chi 投 Headlands Technologies **Software Engineer（Java）**，通过 HackerRank「Headlands Tech Coding Test - Java」，被邀约 **一小时技术视频面（phone screen）**；先签 NDA，再提交多个工作日可用时段。

Chi 的要求（2026-10-14）：**Java 21 + 新特性，越多越好；教科书模式**（`study/TEXTBOOK.md`）。题集规范是 Java 版 `CONVENTIONS.md`，运行/验收用 `tools/jtest.py`。

## 阶段与状态

| 阶段 | 内容 | 状态 | 验收 |
|---|---|---|---|
| P0 | 骨架 + Java 21 工具链（`openjdk@21` brew、JUnit console jar 在 `~/.cache/trellis-java/`） | ✅ | `jtest.py verify` |
| P1 | 三路尽调 `catalog/raw/{github_repos,forums,official_and_process}.md` | ✅ | — |
| P2 | CATALOG（A–G）· RANK 43 行 · PARETO（cut line 第 22 行） | ✅ | `tools/pareto.py catalog/RANK.md --table 总表 --focus 电面` |
| P3 | `loop/LOOP_GUIDE.md`（视频面） | ✅ | — |
| P4 | 题集 + 讲义：oa01 hc02 hc03 hc04 hc05(+hc14) hc06 hc08 ✅；hc01 hc07 进行中 | 进行中 | `python3 tools/jtest.py verify "loop/rounds/*/*"` |
| P5 | `study/10-java21/` J01–J09、J10–J19 进行中；`study/00-foundations/` 待写 | 进行中 | 示例全部 javac 通过 |
| P6 | kq 语言深度题库（C++ 问法 → Java 问法）· 反问 · 故事 | 待做 | — |
| P7 | 第三波题：hc09 hc11 hc13 ld01 · CONTENTS/COVERAGE · README | 待做 | — |

## 公开仓库约束

邮件里的姓名、邮箱、线程 ID、可用时段链接一律不进仓库；时间线只保留到「日期 + 阶段」。

## 下一步（接手就做这个）

1. 收 hc01/hc07、J01–J09、J10–J19 → 跑 `jtest.py verify` + 抽查讲义数字 → commit → LEDGER 加行。
2. 派 `study/00-foundations/`（复杂度、哈希、堆、JMM、JIT/GC、CPU 缓存）与 kq 题库。
3. 第三波题（见 P7），讲义同样教科书模式。
