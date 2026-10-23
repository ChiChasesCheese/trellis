---
id: hl-cq-q19-erase-overview
node: cpp-questions.d-containers
type: qa
step: 12
---
## Q
面试题：怎样正确地从容器里删除元素？（erase-remove 惯用法、循环里删除、`std::erase_if`）
How do you erase elements from a container correctly?

## A
- `std::remove_if` 只是把要保留的元素前移，**不改变容器大小**，所以要接 `erase`（erase-remove 惯用法）。
- 循环里删除要用 `erase` 返回的迭代器。
- C++20 直接 `std::erase_if(c, pred)`。
- 顺序无所谓时，**swap-and-pop** 是 O(1)。
