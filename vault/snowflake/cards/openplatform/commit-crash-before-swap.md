---
id: commit-crash-before-swap
node: openplatform.external-engine-commit-protocol
type: qa
source: snowflake-docs
---
## Q
Spark 作业向 Iceberg 表写入时，数据文件和新元数据文件都写完了，但在更新 catalog 指针之前进程崩溃。表会处于半写入状态吗？会留下什么副作用？

## A
不会出现半写入状态。读者总是通过 catalog 中的当前元数据指针找到快照，而指针还指向旧元数据文件，所以已写出的新文件不属于任何快照，对查询完全不可见，表保持提交前的一致状态。副作用是对象存储中留下孤儿文件（orphan files），占用存储但不影响正确性，需要通过表维护操作（如清理孤儿文件）回收。
