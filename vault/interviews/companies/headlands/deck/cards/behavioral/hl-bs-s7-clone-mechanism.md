---
id: hl-bs-s7-clone-mechanism
node: behavioral.stories
type: qa
step: 38
---
## Q
S7 里零拷贝克隆（zero-copy clone）为什么只要约 2 秒？克隆顺序为什么会弄坏跨库 stream？怎么修？

## A
- **为什么 2 秒**：数据存在**不可变的微分区**（immutable micro-partitions）里；克隆只是让新对象**指向同样的文件**，复制的是**元数据**，不是数据。存储成本只在数据**分叉**之后才出现。
- **跨库 stream 的坑**：先克隆**应用库**，会让依赖**复制库**表的 stream 失效。
- **修法**：固定顺序，**先克隆复制库**，换 slot 之后**自动修复**。
- 另外：修了**重复的可重复迁移**，并为仅生产存在的依赖加了**结构空壳表**（stub tables）。
