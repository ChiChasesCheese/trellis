# study/ — Snowflake kit 的学习面（中文）

> 题库在 `../problems/`（OA）与 `../loop/rounds/`（其余轮次）；这里是**读完就能独立做出来**的路径。与 Stripe 的 `../../stripe/study/` 同一分工：具体题目留在公司 kit，可迁移规律升到 trellis 的 `code-core` / `system-design` 牌组。

## 推荐顺序

| 步骤 | 做什么 | 花多久 |
|---|---|---|
| 1 | `00-prereq/04-snowflake-primitives.md` + `20-cards/snowflake_internals.md`：把自己的 Snowglobe 经验对上 Snowflake 原语 | 1 小时 |
| 2 | `10-rounds/` 按轮次读：先读你下一轮的那一章 | 每章 20 分钟 |
| 3 | `00-essentials/`：解题框架 · DP 模式 · 图/树模式 · 类设计与并发 · SD 框架 | 3 小时 |
| 4 | `30-articles/`：cut line 内每题一篇——**先做题再读**（题解用来验收） | 每题 20 分钟 |
| 5 | `20-cards/`：碎片时间读；`sd_checklist.md` 面试当天贴在旁边 | — |

## 目录

```
study/
  README.md
  INDEX.md                      题 × 考点 × skills_matrix id × 文章 的映射总表
  00-prereq/                    前置：Python 面试写法 · 并发基础 · 分布式词汇 · Snowflake 原语
  00-essentials/                通用精华：01 解题框架 · 02 DP 模式 · 03 图/树模式 · 04 类设计与并发 · 05 SD 框架 + Snowflake 原语
  10-rounds/                    每轮准备：00 AI · 01 recruiter · 02 OA · 03 电面 coding · 04 OOD · 05 SD · 06 expertise · 07 HM · 08 team matching
  20-cards/                     速记卡：patterns · snowflake_internals · sd_checklist
  30-articles/                  每题一篇中文题解（文件名 = 题目目录名）
```

## 与 trellis 牌组的关系

- 通用算法/OOD 规律 → `code-core` 域（`transfer.*` 分支：新公司的一轮面试 = 一个叶子）。
- SD 规律 → `system-design` 域；Snowflake 原语可作为 Case 挂到对应叶子。
- 本目录不建卡；面完把新规律写回牌组。
