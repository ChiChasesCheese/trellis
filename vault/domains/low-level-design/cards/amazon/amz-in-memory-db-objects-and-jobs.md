---
id: amz-in-memory-db-objects-and-jobs
node: amazon.amz-in-memory-db
type: qa
step: 2
tags: [grown]
---
## Q
在内存数据库设计里，需要哪几个核心类？各自只负责什么？

## A
这个系统存若干张类型化的表，按条件查询、连接，并能执行 SQL 文本。

- `Table`：只管存，`{主键: 行}` 字典、列类型、自增计数器；`check` 是类型和主键约束的唯一入口。
- `Pred`（`Cmp` / `In` / `IsNull` / `And` / `Or` / `Not`）：判断一行，返回真、假或未知。
- `Join`：连哪张表、用哪两列、内连还是左连。
- `Database`：表的集合，写操作的原子性和 `select` 流水线。
- `Parser`：只把 SQL 文本翻译成对 `Database` 的调用。
