---
id: hi-c-sd-data-modeling-x03-shard-key
node: sd.core-concepts.data-modeling.exam
type: qa
step: 3
---
## Q
**数据建模 · 选分片键**｜考点 · 必会
聊天应用要存消息。方案 A 按 `message_created_at` 的月份分片，方案 B 按 `conversation_id` 分片。主要查询是"打开某个对话，取最近 50 条"。评价两者。

## A
- **B 更好：** 一个对话的所有消息在同一分片，主查询只访问一个分片，没有跨片合并。
- **A 的问题：** 当月所有写入集中在同一个分片，形成热点；而且一个对话的消息散在多个月份的分片里，取最近 50 条可能要访问两个分片。
- **B 的隐患：** 超大群聊的 `conversation_id` 可能成为热键，需要再加子键（如加一个桶号）分散。
- **分片键基本不可改**，所以要先写下主要访问模式再选。
