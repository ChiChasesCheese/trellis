---
id: foundations-interview-opening-moves
node: foundations.method
type: qa
---
## Q
First five minutes of a system design interview: what two categories of requirements do you pin down, and what form should each take?

## A
- **Functional**: the 3–5 core use cases you will actually design for — explicitly scope out the rest ("I'll focus on posting and the feed; skip search").
- **Non-functional**: expressed as **numbers**, not adjectives — target scale (DAU, QPS), latency budget (e.g. p99 < 200 ms), availability target, read/write ratio, consistency needs.

Numbers matter because they are what later justify each design choice.


## Q zh
系统设计面试前五分钟：你要确定哪两类需求，每类应该用什么形式？

## A zh
- **功能性**：3–5 个你实际会设计的核心用例 — 明确排除其余的（"我会专注于发布和推送流；跳过搜索"）。
- **非功能性**：表示为**数字**，不是形容词 — 目标规模（DAU、QPS）、延迟预算（例如 p99 < 200 ms）、可用性目标、读写比、一致性需求。

数字很重要因为它们是后来为每个设计选择辩护的基础。
