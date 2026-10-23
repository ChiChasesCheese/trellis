---
id: hl-c10-allocator-model
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 8
---
## Q
STL 的分配器（Allocator）模型是什么？最小要实现什么？`std::pmr` 是什么？

## A
- 标准容器的**第二个模板参数**就是分配器：容器所有内存申请经由 `allocate(n)` / `deallocate(p, n)`。换分配器就能改变内存来源（栈缓冲、arena、共享内存、统计）而不改容器代码。
- 最小实现：`value_type`、`allocate`、`deallocate`、重绑定构造 `template <class U> CountingAlloc(const CountingAlloc<U>&)`（节点容器要分配别的类型）、相等性比较 `operator==`/`!=`。
- **C++17 `std::pmr`**：分配器类型固定为 `polymorphic_allocator`，运行期选择 `memory_resource`（如 `monotonic_buffer_resource` 使用给定缓冲区）。
