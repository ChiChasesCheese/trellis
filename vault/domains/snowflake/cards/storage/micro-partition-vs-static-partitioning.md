---
id: micro-partition-vs-static-partitioning
node: storage.micro-partition-format
type: qa
source: snowflake-docs
---
## Q
传统数仓的静态分区（static partitioning）要用专门的 DDL 定义和维护，Snowflake 的微分区（micro-partition）在这点上有什么不同，解决了静态分区的哪两个老问题？

## A
微分区是自动派生的：所有 Snowflake 表都会按数据插入/加载时的顺序被透明地切分，用户无需预先定义也无需维护。它针对静态分区的两个老问题：一是维护开销（不用写分区 DDL、不用手工管理分区）；二是数据倾斜（data skew）导致的分区大小严重不均——微分区大小统一且较小，并且允许值域相互重叠，因此不会出现某个分区异常膨胀。
