---
id: hl-c10-selftest-string-malloc
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 15
---
## Q
自测：对 `std::string` 先 `malloc(sizeof(std::string))`，再 `s->append("x")` 会怎样？`delete` 做哪两件事？placement new 创建的对象谁来析构？

## A
- 是 **UB**：没有运行构造函数，`string` 内部指针/长度是垃圾。
- `delete`：先调**析构函数**，再 `operator delete` 归还内存。
- placement new 的对象：由**你自己**析构（`p->~T()` 或 `std::destroy_at`），内存也由你管理。
