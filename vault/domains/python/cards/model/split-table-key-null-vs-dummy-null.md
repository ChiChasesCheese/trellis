---
id: split-table-key-null-vs-dummy-null
node: model.dict-set-internals
type: qa
source: cpython-internals
---
## Q
拆分表（split table）里 `(key, NULL)` 这种键值组合表示什么状态？它和表示「已删除条目」的 `(<dummy>, NULL)` 有什么区别？

## A
`(key, NULL)` 表示这个键已经存在于共享的 key-table 里，但对应的值还没写入（「待插入」状态），只有在拆分表场景下才会出现；`(<dummy>, NULL)` 表示这个槽位原本有条目、但已被删除，用哨兵值 `<dummy>` 占位以维持开放寻址（open addressing）的探测链不断裂。二者都表示「没有值」，但语义相反：一个是「还没写」，一个是「写过又删了」。
