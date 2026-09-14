---
id: join-choice-heuristic
node: query.join-strategies-broadcast-shuffle
type: qa
tags: [grown]
---
## Q
优化器在广播连接（broadcast join）与洗牌连接（shuffle join）之间选择时，依据的核心数据量启发式是什么？

## A
比较两种方案要移动的数据量和内存需求：广播的代价约为“小表大小 × 节点数”，并要求小表能放进每个节点的内存；洗牌的代价约为“两表大小之和”的重分布。当一侧足够小（估算的行数/字节数低于阈值，且小表 × 节点数明显小于大表）时选广播，否则选洗牌。由于依赖基数估算，估算失准就可能选错策略。
