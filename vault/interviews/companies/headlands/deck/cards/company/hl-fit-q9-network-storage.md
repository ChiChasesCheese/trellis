---
id: hl-fit-q9-network-storage
node: company.fit
type: qa
step: 11
---
## Q
JD 要求 "Good knowledge of networking and storage systems"，你的存储和网络经验各有什么、怎么说、缺什么？

## A
评级：**部分**。

- **存储**：Snowflake（微分区、零拷贝克隆、Streams）、PostgreSQL、Kafka log 的使用者视角。用 Snowflake 的存储模型讲"不可变文件 + 元数据指针"。
- **网络**：Kafka proxy（SASL/TLS 代理）、gRPC 列在 skills；**没有 TCP / 延迟 / 吞吐的亲手经验**。诚实说 "as a user of Kafka and gRPC"，并讲你读过的 Nagle / `TCP_NODELAY`、批量 vs 延迟。
- 要补：存储引擎（B+ 树 / LSM）；TCP 基础。
