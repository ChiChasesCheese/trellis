---
id: hl-c03-array-pointer-pitfall
node: cpp-lessons.c03-smart-pointers
type: qa
step: 13
---
## Q
`unique_ptr<T[]>` 和 `unique_ptr<T>` 在释放上有什么区别？数组该怎么选？

## A
- `unique_ptr<T[]>` 用 `delete[]` 释放；`unique_ptr<T>` 用 `delete`。数组对象用错释放方式是未定义行为。
- 实践上，动态数组直接用 `std::vector`，更安全、带大小、可扩容。
- 其余情况（`shared_ptr` 数组等）同样优先改用 `vector`。
