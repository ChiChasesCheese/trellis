---
id: hl-cq-q19-unordered-set-erase-followups
node: cpp-questions.d-containers
type: qa
step: 16
---
## Q
两个追问：`unordered_map::erase` 使什么失效？为什么不能对 `std::set` 用 `remove`？

## A
- **`unordered_map::erase`**：只使被删元素的迭代器失效。
- **`std::set` 不能用 `remove`**：会重排元素的算法要求元素可修改，而 set 的元素是 const；要用成员函数 `erase`，或 `erase_if`。
