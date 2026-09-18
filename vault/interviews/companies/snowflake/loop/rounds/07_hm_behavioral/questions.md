# HM / Behavioral 轮 —— 题库（30 题，按 8 条价值观分组）

> 来源：`catalog/raw/bq_hm_recruiter.md` §2（U. Miami 镜像 Exponent 2026-05；Aced/Exponent 2026-08；spacecomplexity 2026-06；官方价值观原文 2026-02-23 Code of Conduct）。形式：onsite 一轮 30–45 min，面试官逐题记笔记；早期职业也有独立 BQ 轮（1p3a thread-1113703）。练习：`python3 loop/mock.py bq hm -n 5 -m 3`。
> **一句话**：Own It / Get It Done / Integrity Always 三条最常被问；每个故事要有"我"的动作 + 数字 + 改了什么。

## 价值观 → 题 → 故事

| 价值观（原文关键词） | 典型题 | 主故事 | 备用 | 踩雷点 |
|---|---|---|---|---|
| **Own It**（like it's yours · own issues · own mistakes） | mistake · ownership · production issue · changed a process · without authority | [[S3]] ACH RCA（自己转发 pager 当场根因） | [[S2]]（自己修自己的缺陷）· [[S7]] | 归因外部；讲不出改了什么流程 |
| **Get It Done**（results · precise yet nimble · follow through） | competing deadlines · hard deadline what did you cut · trade-off & debt · ambiguity | [[S8]] 7 分钟 RCA 出 PR | [[S1]] 18 个月生产 · [[S5]] 两年 owner | 只讲赶上了；没说 slip 前先沟通 |
| **Integrity Always**（speak up candidly · disagree then commit fully） | conflict · pushback · bad news · committed to a decision you argued against · changed your mind · disagreed with manager | [[S6]] go/no-go 叫停实习生项目 | [[S2]] ADR · [[S4]] | 把对方说成不讲理；只有 backbone 没有 commit |
| **Put Customers First**（earn trust · listen · pain points） | customer first when inconvenient | [[S4]] AU refund fee（给 PM 同一份证据） | [[S9]] DoorDash SLA | 讲成"客户总是对的" |
| **Be Excellent**（quality · simplicity · today and tomorrow） | raised the bar · high bar when nobody checks · would do differently | [[S5]] shadow-run 0.224% | [[S2]] 框架复用 8 次 | "能跑就行" |
| **Think Big**（ambitious · prudent risks） | most ambitious · prudent risk · why Snowflake why now | [[S5]]（$55B TPV 前提） | Quant-Stroller 66K 行 | 只有大话没有风险控制 |
| **Make Each Other the Best**（help · ask for help · feedback · teach） | teammate grow · asked for help · critical feedback · teamwork · other team | Ziyang（domain-ownership 框定） | onboarding doc 两年 · [[S4]] 跨团队 | 编造 1:1 细节；"从不需要帮助" |
| **Embrace Each Other's Differences** | very different approach | [[S5]] 三方（Pricing Kotlin / Funding Ruby / Fiserv 外部） | Chicago → San Jose | 说成"我忍了" |

## 题目（原文见 bank.json）

| # | 问题原文 | 价值观 | 来源 |
|---|---|---|---|
| 1 | Tell me about a time you made a mistake. What did you learn? | Own It | Exponent 镜像 |
| 2 | Tell me about a time you took ownership over a project, and why. | Own It | 同上 |
| 3 | Work effectively with another team you had never worked with before. | Make Each Other the Best | 同上 |
| 4 | A project you wouldn't have completed without teamwork. | Make Each Other the Best | 同上 |
| 5 | Conflict with a coworker/stakeholder and how you resolved it. | Integrity Always | Aced |
| 6 | Pushed back on a decision you disagreed with. | Integrity Always | Aced |
| 7 | Prioritize between competing deadlines. | Get It Done | Aced |
| 8 | Put the customer first when it was inconvenient. | Put Customers First | Aced |
| 9 | Raised the bar / ownership outside your scope. | Be Excellent | Aced |
| 10–30 | 见 `bank.json`（价值观原文派生 + 通用题） | — | — |

## 作答纪律

- 每故事两版：90 s（默认）/ 3 min（被追问"再展开"）。
- 结构：一句话 → 我做了什么 → 数字 → 改了什么 / 学到什么。
- 少术语：这是行为轮；技术细节留给 expertise 轮。
- 数字只用已确认项（`../../../04-answer-bank.md` §6 数字卡）。
