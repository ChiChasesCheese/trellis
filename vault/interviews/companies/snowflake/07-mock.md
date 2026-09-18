---
title: Snowflake Chakra mock
aliases:
  - Chakra mock
tags:
  - company/snowflake
  - round/ai-screen
---

# 07 · 自测 mock（20 分钟，计时，English）

> 用法：手机计时器 20:00 倒数；按顺序**出声**回答，不看故事笔记（[[S1]]…[[S11]]）的稿，只看 `loop/rounds/00_ai_screen/CARD.md`；每题答完在右列打分。跑两遍，第二遍只跑上一遍 ≤ 2 分的题。
> 自评标准照 Chakra 的 Met 定义：**3** = 有 headline + mechanism + 数字 + 我本人做的部分；**2** = 有故事但缺数字或缺「为什么」；**1** = 泛泛 / 讲原理。

## Round A · 主问（每题首答 ≤ 90 s）

| #   | 段   | 题（英文照读）                                                                                                                                                | 目标故事                   | 自评  |
| --- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- | --- |
| 1   | 经历  | Tell me about yourself and your current role.                                                                                                          | 自我介绍                   | ☐   |
| 2   | 经历  | Walk me through a recent project and your specific contribution.                                                                                       | [[S1]]                     | ☐   |
| 3   | 经历  | What's the hardest technical challenge you've faced, and how did you resolve it?                                                                       | [[S3]]                     | ☐   |
| 4   | 场景  | Suppose a nightly data pipeline that computes customer charges starts producing wrong totals for a subset of customers. How would you find and fix it? | [[S3]] 方法 + scenarios §1   | ☐   |
| 5   | 场景  | How would you design a service that meters usage events and produces a daily bill, so that retries never double-charge?                                | scenarios §2（幂等 / MERGE / 对账） | ☐   |
| 6   | 场景  | You need to change the schema of a large production table without downtime. How do you approach it?                                                    | [[S5]] shadow-run + scenarios §3 | ☐   |
| 7   | 协作  | Describe a technical decision you made and the trade-offs involved.                                                                                    | [[S5]]                     | ☐   |
| 8   | 协作  | Tell me about a time you disagreed with a teammate or another team. What happened?                                                                     | [[S4]] / [[S2]]                | ☐   |
| 9   | 协作  | Tell me about a time you had to push back on a plan or say no.                                                                                         | [[S6]]                     | ☐   |
| 10  | 协作  | How do you decide what to prioritize when several things are urgent?                                                                                   | [[Answers#Q20]] in core/answers    | ☐   |
| 11  | 反问  | Do you have any questions for us?                                                                                                                      | playbook §6            | ☐   |

## Round B · 追问（每答 ≤ 60 s；随机抽 6 个）

1. What part of that did you do yourself, versus the team?
2. Why did you choose that approach over the alternatives?
3. What were the numbers — how did you measure the result?
4. How did you verify it was correct before shipping?
5. What would you do differently if you did it again?
6. What broke afterwards, and what did you learn?
7. Who else was involved, and how did you keep them aligned?
8. What was the biggest risk, and how did you mitigate it?
9. How does that experience apply to the kind of systems Snowflake builds?
10. If the data volume were 100× larger, what would change?

## Round C · 价值观直击（每答 ≤ 60 s；抽 3 个）

| 价值 | 题 |
|---|---|
| Put Customers First | Tell me about a time you changed a technical plan because of what a customer or user actually needed. |
| Integrity Always | Tell me about a time you delivered news people didn't want to hear. |
| Think Big | What's the most ambitious thing you've built or proposed? |
| Be Excellent | How do you hold yourself to a high bar when nobody is checking? |
| Get It Done | Tell me about shipping something under a hard deadline. |
| Own It | Tell me about a production issue you owned end to end. |
| Make Each Other the Best | How have you helped a teammate grow? |
| Embrace Each Other's Differences | Tell me about working with someone whose approach was very different from yours. |

## 录音回听清单

- [ ] 每个首答 ≤ 90 s（用录音时长核）
- [ ] 每个故事至少 1 个数字、1 个工具名、1 句 "I decided / I chose / I wrote"
- [ ] 没有一句以 "In general, the best practice is…" 开头（theoretical = Not Met）
- [ ] 专有名词说清：GRRCN、MERGE、Streams、Tasks、UDTF、Fiserv、interchange
- [ ] 没说 $600B；说了 138B / 22M / 13.7M / 0.224%
- [ ] 每段结尾有 learning / trade-off 一句

## 记录

| 遍次 | 日期 | ≤2 分的题 | 备注 |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
