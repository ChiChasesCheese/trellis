---
id: tc-peers
node: t03.peers
type: qa
step: 1
tags: [原则]
---
## Q
**Peers · 细节与取舍**｜原则 · 必会

你在 design review 里向同组的五个工程师讲分库分表方案。你用了管理层那种三句话版本，结果被连问了十分钟。哪里没对上？

## A
**原则：** 同行要**判断你的方案对不对**，所以需要的是细节和**取舍**：你考虑过哪些方案、为什么排除、有什么代价、哪些地方你不确定。他们的知识大致与你相当，不用解释基础。

**怎么做：**
1. 先说清范围：这份设计覆盖什么、**不**覆盖什么，免得评审跑偏。
2. 写明你考虑过的备选和排除理由。
3. 明确写出代价和未解决的问题。同行更信任说出弱点的人。
4. 对前提不同的同行（别的团队），第一次出现的缩写和内部术语要定义。
5. 用他们熟悉的东西做对比："similar to X, except…"

**常见错法：**
- **只有结论没有过程：** 同行没法验证。
- **只讲优点：** 会被追问，反而显得没想过。
- **默认所有人读过背景：** 别的团队的人跟不上。

**改写示例：**
- Before: "We'll shard by user id. It scales well."
- After: "We'll shard by user id. The upside is even load; the cost is that cross-user queries need scatter-gather. I considered sharding by region, but hot regions skew the load. One open question: how do we re-shard later?"

**出处：** Google Technical Writing One《Audience》《Documents》（developers.google.com/tech-writing/one：scope 与 non-scope、对比已知概念）
