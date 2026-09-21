---
id: dict-sparse-tradeoff
node: memory.object-size
type: qa
source: cpython-internals
---
## Q
把 dict 内部哈希表做得更稀疏（sparse，多留空位、少装填）对性能有什么两面的影响？

## A
更稀疏能减少哈希碰撞（collision），让单个 key 的读写更快；代价是遍历变慢——`keys()`/`items()`/`values()`/`__iter__()` 等操作要扫描每一个潜在槽位（包括空位），dict 容量翻倍后这些遍历操作要多访问一倍且更不连续的内存。
