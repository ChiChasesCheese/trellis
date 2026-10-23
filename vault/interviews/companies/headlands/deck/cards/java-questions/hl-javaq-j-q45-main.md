---
id: hl-javaq-j-q45-main
node: java-questions.j-storage
type: qa
step: 6
---
## Q
分布式存储：复制、一致性，以及 LSM 树与 B 树的取舍。为研究数据设计存储层，你会考虑什么？
Distributed storage: replication, consistency and the trade-offs between LSM trees and B-trees. What would you think about when designing a storage layer for research data?

## A
一句话：先问需求（读写比、延迟 vs 吞吐、顺序 vs 随机、一致性、规模、故障容忍），再选：**B 树**读友好、原地更新、随机写；**LSM 树**写友好（顺序追加 + 后台合并），读放大和合并放大要管；跨机器用复制（同步 / 异步）或纠删码，用共识（Raft / Paxos）保证一致，权衡 CAP 与延迟。

研究数据特征（量化研究平台）：一次写多次读、按时间 / 品种分区、列式压缩、批量扫描为主——更像"**不可变文件 + 元数据索引**"（Parquet 类思路），而不是通用事务数据库；热数据放本地 NVMe / page cache，冷数据放对象存储。
