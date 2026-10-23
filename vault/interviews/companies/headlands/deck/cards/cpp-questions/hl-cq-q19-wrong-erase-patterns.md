---
id: hl-cq-q19-wrong-erase-patterns
node: cpp-questions.d-containers
type: qa
step: 15
---
## Q
`for (auto x : v) if (...) v.erase(...)` 和 `v.erase(it); ++it;` 这两种写法为什么错？`vector::erase` 的复杂度？`map` / `set` / `list` 删除时循环怎么写？

## A
- **range-for 里改容器**：迭代器失效，未定义行为。
- **`v.erase(it); ++it;`**：`it` 在 `erase` 后已经失效。
- **`vector::erase`** 是 O(n)（后面元素前移），从末尾删是 O(1)。
- **`map` / `set` / `list`**：`erase(it)` 只让被删的那个迭代器失效，循环模式是 `it = m.erase(it)`。
