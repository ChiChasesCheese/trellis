---
id: clone-billing-initially-free
node: continuity.clone-storage-billing
type: qa
tags: [grown]
---
## Q
对一张 5 TB 的表执行零拷贝克隆（zero-copy clone）后，账户存储账单会立刻增加 5 TB 吗？为什么？

## A
不会。克隆只是在元数据中新建一个表对象，让它引用源表现有的同一批微分区（micro-partition，不可变的列式数据文件），并不复制任何数据文件。刚创建时两张表共享全部分区，这些分区的存储只按一份计费，所以克隆本身几乎不增加存储费用。
