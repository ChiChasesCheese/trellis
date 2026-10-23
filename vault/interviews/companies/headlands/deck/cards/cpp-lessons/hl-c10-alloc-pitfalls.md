---
id: hl-c10-alloc-pitfalls
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 14
---
## Q
`new`/`malloc`/分配器相关有哪八个常见的坑？

## A
1. `new[]` 配 `delete`（缺 `[]`）= UB。
2. 手动 `delete` 后继续用指针 / 再次 `delete`（置 `nullptr` 只缓解）；所以用智能指针。
3. 在 `malloc` 的内存上直接当对象用（没有构造）。
4. placement new 用未对齐的缓冲区。
5. 忘记调用析构函数，导致资源泄漏。
6. `new` 抛异常时构造到一半的对象：成员 RAII 保证无泄漏。
7. 池/arena 中对象的指针在 `reset` 后悬空。
8. 自定义分配器要满足 rebind 和相等性比较。
