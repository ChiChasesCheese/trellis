---
id: hi-sd-dynamodb-3-access
node: sd.deep-dives.dynamodb
type: qa
step: 3
---
## Q
**DynamoDB：Query、Scan 与按条目读取**｜系统设计 · 深入技术

在 DynamoDB 里读数据有哪两种基本操作？为什么要尽量避免 Scan，ProjectionExpression 能省钱吗？

## A
**两种操作。**
- Query：按主键或索引键条件读取，只读匹配的条目，可在排序键上做范围查询
- Scan：读取表或索引的每个条目并分页返回，大数据集上很低效，应尽量避免

**怎么避免 Scan。** 靠数据建模：选对分区键和排序键，让访问模式都能走 Query。主要接口是 SDK 或控制台；也支持 PartiQL（兼容 SQL 的语法），但它只是便利层，底层仍翻译成同样的操作。

**易错。** ProjectionExpression 只减少网络传输。整个条目照样从存储读取，读容量按条目总大小计费。这与 SQL 选列不同。

**建模含义。** 大条目要拆分。例如设计 Yelp，商家表若内嵌评论列表，读商家名称和地址时也要读出所有评论；应把评论拆成单独的表，按 business_id 查询。
