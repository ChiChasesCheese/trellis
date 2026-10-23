---
id: hl-c05-address-stability
node: cpp-lessons.c05-stl-containers
type: qa
step: 10
---
## Q
实测哪些容器操作之后"第一个元素的地址不变"？`vector` 在容量满和有余量时、`deque`、`list`、`map`、`unordered_map` rehash 各是什么结果？

## A
- `vector` 容量已满时 `push_back`：地址**变了**（`false`，必须重分配）。
- `vector` 有余量（`reserve(100)`）时 `push_back`：地址**不变**（`true`）。
- `deque` 连续 `push_back` 1000 次：元素地址不变（`true`），但迭代器失效。
- `list`、`map` 插入 1000 个：地址不变（节点容器）。
- `unordered_map` 插入 1000 个导致 rehash（桶数 2 → 1597）：元素地址**不变**，迭代器失效。
- 结论：需要稳定地址就 `reserve` 够、用 `deque`/`list`/`map`、或存下标。
