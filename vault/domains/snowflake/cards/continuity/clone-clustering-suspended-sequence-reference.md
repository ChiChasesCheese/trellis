---
id: clone-clustering-suspended-sequence-reference
node: continuity.zero-copy-clone
type: qa
source: snowflake-docs
---
## Q
单独克隆一张带聚簇键（clustering key）、并且某列默认值引用序列（sequence）的表，克隆表在自动聚簇和序列上有哪两个容易踩坑的默认行为？

## A
1) 克隆表保留聚簇键，但自动聚簇（Automatic Clustering）默认被挂起，需要手动 `ALTER TABLE … RESUME RECLUSTER`。2) 只克隆表本身（或序列在另一个数据库/模式中）时，克隆表仍引用源序列，与源表共用一个序列取值；只有克隆同时包含表和序列的数据库或模式时，克隆表才引用克隆出的序列。
