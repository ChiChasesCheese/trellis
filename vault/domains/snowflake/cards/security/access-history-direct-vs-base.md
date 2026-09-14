---
id: access-history-direct-vs-base
node: security.data-lineage-and-access-history
type: qa
tags: [grown]
---
## Q
用户通过视图 `v_orders` 查询了数据，`ACCESS_HISTORY`（ACCOUNT_USAGE 中记录每条查询读写了哪些对象和列的审计视图）会怎样记录？为什么要区分两种“访问对象”？

## A
它同时记录 `DIRECT_OBJECTS_ACCESSED`（查询文本里直接引用的对象，这里是视图 `v_orders`）和 `BASE_OBJECTS_ACCESSED`（最终真正被读到的底层表和列）。区分二者是因为审计要回答“谁实际读了哪张表的哪一列”：只看直接对象会被视图、嵌套视图挡住，看不到敏感表被间接读取；只看底层对象又不知道用户是通过哪个入口访问的。
