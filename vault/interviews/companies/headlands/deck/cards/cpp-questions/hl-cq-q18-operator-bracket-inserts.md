---
id: hl-cq-q18-operator-bracket-inserts
node: cpp-questions.d-containers
type: qa
step: 8
---
## Q
对 `std::map` 读取 `m["missing"]` 会发生什么？查找应该用什么？`try_emplace` 调两次保留哪个值？rehash 之后引用还有效吗？

## A
- `operator[]` 会**插入**默认值：读 `m["missing"]` 之后 `size=1`、值为 0。
- 只查找不改变容器：用 `find`（或 `contains`），`find("other")` 返回 `end`，`size` 不变。
- `try_emplace` 调两次**保留第一个值**。
- `map` 按 key 顺序遍历。
- `unordered_map` rehash 时桶数变化（实测 2 → 1597）而**对元素的引用仍然有效**（读到 100）。
