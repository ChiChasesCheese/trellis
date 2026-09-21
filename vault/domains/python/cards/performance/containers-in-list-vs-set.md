---
id: containers-in-list-vs-set
node: performance.containers
type: qa
source: cpython-internals
---
## Q
同样是判断某个元素是否存在（`x in container`），用 `list` 和用 `set`/`dict` 的复杂度为什么不一样？

## A
`x in list` 要从头线性扫描逐个比较，是 O(n)；`x in set`（或 `dict` 的键）是先对 `x` 计算哈希值、直接定位到哈希表的槽位，平均是 O(1)（最坏情况因哈希冲突退化为 O(n)，但正常分布下极少发生）。频繁做存在性判断时应把数据放进 set 而不是 list。
