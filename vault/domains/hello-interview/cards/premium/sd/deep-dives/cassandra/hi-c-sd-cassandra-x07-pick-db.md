---
id: hi-c-sd-cassandra-x07-pick-db
node: sd.deep-dives.cassandra.exam
type: qa
step: 7
---
## Q
**Cassandra · 三个场景选哪个数据库**｜考点 · 必会

对三个系统分别选 Cassandra、DynamoDB 或 Postgres 并说明理由：(1) 日写入 50 亿条消息、按会话读最近消息；(2) 银行账户间转账；(3) 要自己管基础设施、已有 Kubernetes 集群的海量时序点位。

## A
- **(1) Cassandra 或 DynamoDB：** 写入量大、按会话分区读取、可用性优先，正是它们的强项；用时间桶控制分区大小。纯 AWS 且不想运维时选 DynamoDB。
- **(2) Postgres：** 转账要多行原子、强一致，需要 ACID 事务；Cassandra 只保证单分区的行级原子。
- **(3) Cassandra：** 自己运维、有地域扩展和写入吞吐需求，LSM 树加水平扩展匹配。DynamoDB 是托管服务，没有自己运维的需要。
- **判断顺序：** 先看一致性与事务需求，再看写入规模，最后看谁来运维。
