---
id: hl-c05-list-vs-vector-insert
node: cpp-lessons.c05-stl-containers
type: qa
step: 23
---
## Q
中间频繁插入删除时，应该用 `vector` 还是 `list`？

## A
- 理论上 `list` 在已有迭代器时中间插删是 O(1)，`vector` 要 O(n) 搬移。
- 实际上 `vector` 的搬移是连续内存拷贝，通常仍比 `list` 每步的缓存未命中快（乱序 `list` 遍历约 60 ns/元素 vs `vector` 0.04 ns）。
- 例外：元素**很大**，或者必须保持迭代器/地址**稳定**。
- 默认还是 `vector`。
