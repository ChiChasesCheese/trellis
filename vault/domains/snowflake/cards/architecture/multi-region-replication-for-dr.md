---
id: multi-region-replication-for-dr
node: architecture.cloud-agnostic-multi-region
type: qa
source: snowflake-docs
---
## Q
Snowflake 账户所在的某个云区域整体故障时，要想业务继续运行，需要事先依赖什么机制？为什么不能指望同区域内的存储冗余？

## A
需要事先配置跨区域的 replication（复制），这是 Snowgrid（跨区域、跨云技术层）提供灾难恢复与业务连续性的手段。账户的数据和计算都落在某个具体区域的云基础设施上，同区域的冗余挡不住整个区域不可用；只有把数据预先复制到另一个区域（甚至另一个云厂商），才能在故障时切过去。
