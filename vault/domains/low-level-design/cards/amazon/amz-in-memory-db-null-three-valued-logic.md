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
**用三值逻辑，和 SQL 的结果保持一致**

- **例子**：列 `a` 五行依次是 1、2、NULL、4、NULL（id 1 到 5）；
- **直接比较会错**：Python 里 `None != 2` 为真，于是 `a <> 2` 会把 NULL 行也选出来（id 1、3、4、5），和真正的数据库不一样；`NOT IN (1, NULL)` 同样会多选；
- **三值逻辑**：和 NULL 比较的结果是「未知」，`AND`、`OR`、`NOT` 按真值表计算，WHERE 只保留结果严格为真的行；这样 `a <> 2` 只选出 id 1、4；
- **找 NULL 要专门写**：`a = NULL` 永远是未知、什么都选不出，要写 `a IS NULL`，得到 id 3、5；
- **代价**：谓词的返回值从 `bool` 变成 `bool | None`，每个运算符都要处理「未知」这第三种值。
