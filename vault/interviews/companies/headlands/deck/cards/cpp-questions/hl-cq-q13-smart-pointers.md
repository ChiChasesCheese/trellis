---
id: hl-cq-q13-smart-pointers
node: cpp-questions.c-memory-ownership
type: qa
step: 12
---
## Q
面试题：什么是智能指针？比较 `unique_ptr`、`shared_ptr` 和 `weak_ptr`。
What are smart pointers? Compare `unique_ptr`, `shared_ptr` and `weak_ptr`.

## A
智能指针是 RAII 的指针。**默认用 `unique_ptr`**。
- **`unique_ptr`**：独占所有权；和裸指针一样大（8 字节），零开销，只能移动。
- **`shared_ptr`**：共享所有权；引用计数放在控制块里，16 字节，计数是**原子操作**。
- **`weak_ptr`**：观察 `shared_ptr` 管理的对象但不延长它的寿命，用来打破循环引用。

实测：`sizeof` 裸指针 8、`unique_ptr` 8、`shared_ptr` 16；移动后源 `unique_ptr` 为空。
