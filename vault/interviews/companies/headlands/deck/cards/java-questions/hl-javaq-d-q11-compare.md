---
id: hl-javaq-d-q11-compare
node: java-questions.d-memory
type: qa
step: 4
---
## Q
从分配、初始化、释放、失败方式、碎片、栈上对象六个方面，对比 C++ 的 `malloc` / `new` 与 Java 的 `new`。

## A
- **分配**：C++ 由分配器找空闲块，可能加锁或系统调用；Java 在 TLAB 里指针碰撞，通常无锁。
- **初始化**：`malloc` 不初始化，`new` 调构造；Java 一律清零再构造。
- **释放**：C++ 手动 `free / delete` 或 RAII；Java 靠 GC，不能手动。
- **失败**：C++ 是 `NULL` 或 `bad_alloc`；Java 是 `OutOfMemoryError`。
- **碎片**：C++ 会产生；Java 的复制 / 整理式 GC 无碎片（代价是搬迁对象）。
- **栈上对象**：C++ 默认；Java 只能靠逃逸分析"优化出来"，不是语义保证。
