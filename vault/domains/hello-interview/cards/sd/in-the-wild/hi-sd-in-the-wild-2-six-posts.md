---
id: hi-sd-in-the-wild-2-six-posts
node: sd.in-the-wild.in-the-wild.exam
type: qa
step: 2
---
## Q
**六个案例各演示什么**｜系统设计 · 真实案例

系统设计的真实系统案例有六篇：Meta 的数据库客户端扩展、Figma 的多人编辑、Spotify 的数据湖点查、Slack 的作业队列、Discord 的消息存储、Shopify 的库存预留。请说出每篇对应的模式与技术。

## A
| 案例 | 模式 | 技术 |
|---|---|---|
| Meta：5 种技术把数据库扩展到百万客户端 | 读扩展、写扩展 | 未标 |
| Figma：用简化 CRDT 做多人编辑 | 竞争处理、实时更新 | 未标 |
| Spotify：从 EB 级数据湖提供点查 | 读扩展 | DynamoDB |
| Slack：在 Redis 作业队列前加 Kafka | 长任务、写扩展 | Kafka、Redis |
| Discord：数万亿消息迁到 ScyllaDB | 读扩展、竞争处理 | Cassandra |
| Shopify：库存预留从 Redis 迁到 MySQL | 竞争处理、写扩展 | Redis、PostgreSQL |

**注意。** Discord 的 ScyllaDB 与 Cassandra 兼容，所以归在 Cassandra 技术下；Shopify 的 MySQL 在这里归入关系型数据库一类，标的是 PostgreSQL。

**要点。** 从标题就能看出三篇是存储或队列的替换或加缓冲：Slack 前面加 Kafka，Discord 换存储，Shopify 换库。
