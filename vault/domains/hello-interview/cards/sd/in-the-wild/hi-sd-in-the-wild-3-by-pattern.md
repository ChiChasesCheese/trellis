---
id: hi-sd-in-the-wild-3-by-pattern
node: sd.in-the-wild.in-the-wild.exam
type: qa
step: 3
---
## Q
**按模式反查案例**｜系统设计 · 真实案例

想用真实案例佐证系统设计里的某个模式时，读扩展、写扩展、竞争处理、实时更新、长任务这五个模式分别对应哪几篇案例？

## A
**读扩展（Scaling Reads）。** Meta 的数据库客户端扩展、Spotify 的数据湖点查、Discord 的消息存储。

**写扩展（Scaling Writes）。** Meta 的数据库客户端扩展、Slack 的作业队列、Shopify 的库存预留。

**竞争处理（Dealing with Contention）。** Figma 的多人编辑、Discord 的消息存储、Shopify 的库存预留。

**实时更新（Real-time Updates）。** Figma 的多人编辑。

**长任务（Managing Long Running Tasks）。** Slack 的作业队列。

**技术反查。** Redis：Slack、Shopify；Kafka：Slack；Cassandra：Discord；DynamoDB：Spotify；PostgreSQL：Shopify。

**用法。** 一个案例往往同时对应多个模式，如 Shopify 同时涉及竞争和写扩展，说明真实问题很少只落在一个模式里。
