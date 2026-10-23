---
id: hl-c04-vector-noexcept
node: cpp-lessons.c04-move-semantics
type: qa
step: 7
---
## Q
面试问：为什么 `vector` 扩容时有时拷贝有时移动？为什么自己写的移动操作要标 `noexcept`？
Interview question: Why does `vector` sometimes copy and sometimes move elements when it grows?

## A
- 扩容要把旧元素搬到新内存。如果移动构造**可能抛异常**，搬到一半失败就无法恢复原状。
- 所以 `vector` 用 `move_if_noexcept`：只在移动构造 `noexcept` 时才**移动**，否则为了**强异常保证**退回到**拷贝**。
- 实测增长序列：移动构造 `noexcept` 时输出 `mmm`（三次移动），不标 `noexcept` 时输出 `ccc`（三次拷贝）。
- 结论：自己写的移动构造/赋值务必标 `noexcept`，否则容器里拷贝的成本悄悄回来。
