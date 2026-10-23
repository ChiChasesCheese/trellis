---
id: hl-fit-d2-distributed-storage
node: company.fit
type: qa
step: 14
---
## Q
JD 日常工作 "Design, implement, and maintain distributed storage systems with various performance and reliability requirements"，你没做过时怎么答？

## A
评级：**缺口**。没有自建存储系统的经验；相邻的是对 Snowflake / Kafka / PostgreSQL 的**使用与取舍**（幂等、四层 MERGE、ADR 的容量分析）。

- 说法："I haven't built a storage engine. I've designed on top of three of them and had to know their failure modes."
- 然后讲一个具体失败模式：at-least-once 重投 → 幂等；stream offset 与业务写入不是同一事务。
- 追问到副本、一致性协议、compaction 就说不到，要诚实。
- 要补：Kafka 日志模型、幂等；LSM / B+ 树取舍。
