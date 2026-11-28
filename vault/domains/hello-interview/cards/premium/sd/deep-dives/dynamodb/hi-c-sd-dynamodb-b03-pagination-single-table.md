---
id: hi-c-sd-dynamodb-b03-pagination-single-table
node: sd.deep-dives.dynamodb.beyond
type: qa
step: 3
---
## Q
**DynamoDB · 查询分页与"单表设计"**｜拓展 · 加分

一次 Query 能返回多少数据？有人把所有实体放进同一张表（单表设计），利弊是什么？

## A
- **分页：** 单次 Query 或 Scan 最多返回 1 MB 数据，超过就带着 `LastEvaluatedKey` 返回，客户端用它作为 `ExclusiveStartKey` 继续取下一页；`Limit` 只限制评估的项数，不保证凑满一页。
- **单表设计：** 用通用的 `PK`、`SK` 属性，让一个用户、他的订单、订单行这些不同实体共享分区键，一次 Query 就能把相关实体取回，省掉多次往返，也避免关系库里的 JOIN。
- **利：** 读取次数少、延迟低；一张表的容量管理更简单。
- **弊：** 访问模式一旦改变，重新建模很痛苦；数据可读性差，工具和分析不友好；需要预先把所有访问模式列清楚。
- **取舍：** 需求稳定、延迟敏感时单表设计好；团队还在探索需求时，多张表更容易演进。
