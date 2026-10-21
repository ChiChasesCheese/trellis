---
id: amz-in-memory-db-null-three-valued-logic
node: amazon.amz-in-memory-db
type: qa
step: 5
tags: [grown]
---
## Q
在内存数据库的 WHERE 里，直接用 Python 的 `None` 比较，还是用三值逻辑？各自的代价，以及怎么选？

## A
列 `a` 五行是 1、2、NULL、4、NULL。

直接比较：`None != 2` 为真，`a <> 2` 会选出 NULL 行（id 1、3、4、5），和 SQL 不一致；`NOT IN (1, NULL)` 也会选出一堆行。

三值逻辑：和 NULL 比较是未知，`AND` / `OR` / `NOT` 按真值表算，WHERE 只留结果 `is True` 的行。于是 `a <> 2` 只选 id 1、4，`a = NULL` 为空，要写 `a IS NULL`（id 3、5）。

选三值逻辑，代价是谓词返回 `bool | None`。
