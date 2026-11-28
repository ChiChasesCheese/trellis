---
id: hi-c-sd-dynamodb-x09-find-errors
node: sd.deep-dives.dynamodb.exam
type: qa
step: 7
---
## Q
**DynamoDB · 找出三个过时说法**｜考点 · 必会

有人说："(1) DynamoDB 是 AP 系统，所以不能做强一致读；(2) NoSQL 没有事务，所以订座不能用它；(3) 用 ProjectionExpression 只取名字，读取成本就低很多。"逐条指出错误。

## A
- **(1) 错：** 一致性按每次读选择，设置 `ConsistentRead=true` 就是强一致，读容量翻倍；只有 GSI 读不支持强一致。
- **(2) 错：** 支持 ACID 事务，最多 100 个项、可跨表，可串行化隔离。
- **(3) 错：** 投影只省网络传输，整项仍被读取，按整项大小计 RCU。要省成本，应把大字段拆到另一张表。
- **senior 补充：** 强一致读和事务都更贵，只在需要的路径使用。
