---
id: hl-javaq-d-q11-cpp-side
node: java-questions.d-memory
type: qa
step: 1
---
## Q
C++ 里 `malloc` 和 `new` 有什么区别？各自失败时怎么表现、用什么释放？

## A
- **`malloc`**：只分配**未初始化的字节**，返回 `void*`，失败返回 `NULL`，用 `free` 释放。
- **`new`**：分配内存并**调用构造函数**，类型安全，失败抛 `bad_alloc`，用 `delete`（会调用析构函数）释放。
- 分配本身要由分配器（ptmalloc、jemalloc 等）找空闲块，可能加锁或系统调用，释放要手动或靠 RAII。
- 面试官问 Java 的 `new` 时常顺口问这一侧，先答清楚再对比。
