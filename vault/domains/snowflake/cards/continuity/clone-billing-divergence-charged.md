---
id: clone-billing-divergence-charged
node: continuity.clone-storage-billing
type: qa
tags: [grown]
---
## Q
克隆出来的开发表随后被执行了一次覆盖一半数据的 UPDATE。存储费用如何变化？这由什么机制决定？

## A
微分区（micro-partition）不可变，UPDATE 会为克隆表写出新的分区来替代被改动的分区。这些新分区只属于克隆表，按克隆表的存储单独计费，大约相当于被改写那部分数据的大小；两表仍共享的未改动分区继续只算一份。克隆越偏离源表，额外存储就越多。
