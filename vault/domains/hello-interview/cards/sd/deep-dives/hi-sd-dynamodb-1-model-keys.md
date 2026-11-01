---
id: hi-sd-dynamodb-1-model-keys
node: qb.sd.messenger-chat-system.pre-sd-deep-dives-dynamodb
type: qa
step: 1
---
## Q
**DynamoDB：数据模型与主键**｜系统设计 · 深入技术

DynamoDB 的数据模型和主键怎么设计？分区键（partition key）和排序键（sort key）在底层各自如何工作？聊天应用该怎么选键？

## A
**模型。** 表（table）里有多个条目（item，相当于行），每个条目由属性（attribute）组成，单条目最大 400KB。无需预先定义模式（schema-less），同表的条目可以有不同属性，但数据校验要由应用负责。

**主键。** 必填，由一个或两个属性组成。
- 分区键：对其值做哈希，决定条目存在哪个分区；请求路由器查分区元数据服务得到存储节点，这是集中式分区映射，不是 2007 年 Dynamo 论文的点对点哈希环
- 排序键（可选）：同一分区内按它建 B 树，支持范围查询和有序读取

**选键。** 分区键要贴合最常见的查询，并让数据均匀分布；要范围查询或排序就加排序键。群聊例子：chat_id 作分区键，message_id 作排序键，可按时间读取一个群的全部消息。

**易错。** 排序键用单调递增 ID 而不是时间戳，因为同一毫秒可能有多条消息，时间戳无法保证唯一。可用每分区自增计数、UUID v7（时间在前、可排序，且不暴露 MAC 地址）、Snowflake ID 或 ULID。
