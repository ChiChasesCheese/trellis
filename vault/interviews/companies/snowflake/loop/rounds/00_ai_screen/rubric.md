---
title: Chakra rubric
aliases:
  - Chakra rubric
tags:
  - company/snowflake
  - round/ai-screen
---

# rubric · Chakra 怎么打分，自评怎么打

> 官方机制（`../../../raw/chakra.md` §2）：Creator agent 把 JD 变成 sections + expectations；Interviewer agent 按 plan 问；**Reporter agent 事后只读 transcript**，每条 expectation 独立打 **3 / 2 / 1 / 0**，再归一到 0–5 给 recruiter；**JD 里标 Must have 的要求加权**。人（Talent Acquisition）读报告后决定是否进 recruiter call。

## 官方四档

| 分 | 官方定义 | 对答题的含义 |
|---|---|---|
| **3 Met** | Concrete evidence of clarity, ownership, structured reasoning, specific examples | 有 headline、有原语名/工具名、有 "I decided / I designed"、有量级、有 learning |
| **2 Partially Met** | Some relevant evidence, but lacking depth or specificity | 有故事但缺"为什么"或缺量级 |
| **1 Not Met** | Incorrect reasoning or only vague, theoretical answers | 以 "In general, best practice is…" 开头的回答 |
| **0 Not Assessed** | No relevant transcript moment exists | 没被问到 / 没说到 = 0，不是中性 |

推论：(a) 主动把 rubric 关键词说出口（JD 的 **SQL · distributed systems · Java · database internals · large-scale production**）；(b) theoretical = Not Met，每题必须落到做过的事；(c) 口误无所谓，**被转错的专有名词**会伤分——GRRCN、MERGE、Streams、Tasks、UDTF、Fiserv、interchange 说慢、说清。

## 自评（`../../../07-mock.md` 用这个）

每题录音回听，按下面打 3/2/1：

- **3**：headline ≤ 1 句 → mechanism 带 ≥ 2 个原语名 → 一句 "I decided/designed/owned" → 一个量级 → 一句 trade-off 或 learning；首答 ≤ 90 s；命中 ≥ 2 条 JD 线。
- **2**：故事对，但缺量级、缺"为什么选它"、或超过 2 分钟。
- **1**：讲原理、讲团队、没有"我"。

录音回听清单：
- [ ] 每个首答 ≤ 90 s（用录音时长核）
- [ ] 每个故事至少 1 个量级、2 个原语/工具名、1 句 "I decided / I chose / I wrote"
- [ ] 没有一句以 "In general, the best practice is…" 开头
- [ ] 每段结尾有 learning / trade-off 一句（fail loudly · same SQL for validation and production · deploy ≠ release · config over code · strictest wins）
- [ ] 每个回答至少命中两条 JD 线
- [ ] 没说 $600B；数字都带 "roughly / about"

## 这轮不评什么

无 coding（一手报告 ×3）；不评算法；不评英语口音（transcript 打分）。所以时间全部投给：故事 → 追问版 → 场景骨架 → 关键词卡。
