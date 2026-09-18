# 07 · HM / Behavioral（30–45 min）

> 事实层在 `../../loop/LOOP_GUIDE.md` §8；题库 `../../loop/rounds/07_hm_behavioral/`（30 题）；故事矩阵 `stories.md`；英文答案 `../../../04-answer-bank.md`；中文逐题 [[Answers]]。

## 这轮到底考什么（一句话）

**8 条价值观各有一个带数字、带"我"、带改变的故事。** Own It / Get It Done / Integrity Always 最常；面试官逐题记笔记；onsite 每轮都要 Hire。

## 八条 × 一句证据（背熟）

| 价值观 | 故事 | 一句证据 |
|---|---|---|
| Own It | [[S3]] | "I forwarded the page to myself and posted the root cause the same hour." |
| Get It Done | [[S8]] | "Seven minutes from alert to PR; the release shipped." |
| Integrity Always | [[S6]] | "I wrote down that the detector wasn't prod-ready — 834M rows in QA vs 39B in prod — and froze the work." |
| Put Customers First | [[S4]] | "I gave the PM the exact query so she could verify it herself." |
| Be Excellent | [[S5]] | "0.224% variance over 13.7M rows, every category explained, before we switched." |
| Think Big | [[S5]] | "The prerequisite for about $55B of incremental volume." |
| Make Each Other the Best | Ziyang | "His exclusion service and journaling sync integrate into the domain I own; I define the contracts." |
| Embrace Differences | [[S5]] | "Three teams, three languages — Kotlin, Ruby, and an external partner — one reconciliation." |

## 练法

```bash
python3 loop/mock.py bq hm -n 5 -m 3 --seed 1
```

每题 90 秒默认版；被追问才用 3 分钟版；讲完对 `rubric.md` 六维打分；5 题一组检查价值观覆盖（`stories.md`）。

## 结构（每题同一个）

**一句话结论 → 我做了什么（动词）→ 数字 → 改了什么 / 学到什么。**
disagree 类题最后一定落在 **commit**：价值观原文是 "Commit fully when decisions are made"。

## 挂点 → 对策

| 挂点 | 对策 |
|---|---|
| 同一个故事答 5 题 | 矩阵里每条价值观至少两个故事可切 |
| "我们" | 动词主语改成 I |
| 冲突题把对方说成不讲理 | 先说对方合理的顾虑 |
| mistake 题选太轻的 | 用 [[S2]]：自己设计的框架 4% 失败阻塞全部商户，自己写 ADR 改掉 |
| 技术术语堆砌 | 行为轮少术语，技术细节留给 expertise 轮 |
