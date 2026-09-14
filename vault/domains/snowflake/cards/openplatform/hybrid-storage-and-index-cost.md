---
id: hybrid-storage-and-index-cost
node: openplatform.hybrid-tables-oltp
type: qa
source: snowflake-docs
---
## Q
把一张大表从标准表迁到混合表（hybrid table）后，存储占用明显变大，写入也略慢。原因分别是什么？

## A
存储变大：混合表的主存储是行存，而标准表的列式数据压缩率通常高得多，所以混合表的存储占用一般更大（还叠加异步复制到对象存储的副本）。写入开销：混合表的索引在写入时同步更新，以保证点查立即可用；标准表上的搜索优化服务（Search Optimization Service）则是批量异步维护。这是用写入和存储成本换取低延迟点读与强约束。
