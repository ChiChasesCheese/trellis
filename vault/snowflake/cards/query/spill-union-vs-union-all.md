---
id: spill-union-vs-union-all
node: query.spilling-to-remote-disk
type: qa
source: snowflake-docs
---
## Q
一个把两张大表合并的查询写成了 `UNION`，结果大量溢出（spilling）到磁盘。如果业务上不需要去重，改成 `UNION ALL` 为什么可能消除溢出？

## A
`UNION ALL` 只是把两个输入拼接起来；`UNION` 在拼接之外还要做重复消除，在查询画像（Query Profile）里表现为 UnionAll 算子上方多出一个 Aggregate 算子。对海量数据做去重正是中间结果容易超出内存、引发溢出的典型操作。语义允许时改用 `UNION ALL`，就去掉了这一步去重，也就去掉了需要大量内存的中间结果。
