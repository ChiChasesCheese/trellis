---
id: kafka-streams-stream-table-duality
node: streams.concepts
type: qa
source: kafka-2e
---
## Q
流和表可以看作「同一枚硬币的两面」。把一张数据库表转成一条事件流、以及把一条事件流转成一张表，分别对应什么操作？

## A
表（table）保存的是数据在某一时刻的当前状态（比如客户当前的联系方式），流（stream）保存的是导致状态变化的一系列历史事件（比如每一次联系方式的修改记录）。把表转成流，需要捕获这张表发生过的所有 insert、update、delete 变更事件并依次写入流，这通常靠数据库的 CDC（change data capture，变更数据捕获）方案配合 Kafka 连接器实现。把流转成表则叫作**物化**（materialization）：从头到尾遍历流里的每一个事件，依次应用到内存、内部状态存储或外部数据库里的一张表上，遍历完成后这张表就代表了截止到最后一个事件为止的当前状态。
