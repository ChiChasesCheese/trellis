---
id: hl-fit-q6-abstraction-levels
node: company.fit
type: qa
step: 8
---
## Q
JD 要求 "Comfortable operating at various levels of abstraction, from individual machines to large scale distributed systems"，你该怎么回答？有什么缺口？

## A
评级：**部分**。

- 高层有证据：Kafka、K8s 部署形态、Snowflake、Spark；也往下一层走过，例如零拷贝克隆为什么 2 秒（微分区元数据）、并行度 = replicas × tasks.max 且受 partition 数限制。
- **缺口**：简历没有单机层面（CPU、内存、磁盘、内核）的证据。
- 说法："Most of my work has been at the distributed-service and data-warehouse level… I'm deliberately learning the single-machine layer: caches, syscalls, the JVM."
- 不要说 "all levels"。补课顺序：CPU 缓存局部性 → 进程 / 线程 / IPC。
