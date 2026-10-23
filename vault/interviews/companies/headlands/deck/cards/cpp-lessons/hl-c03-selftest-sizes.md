---
id: hl-c03-selftest-sizes
node: cpp-lessons.c03-smart-pointers
type: qa
step: 15
---
## Q
`sizeof(unique_ptr<int>)` 和 `sizeof(shared_ptr<int>)` 在 64 位平台各是多少？为什么？

## A
- `unique_ptr<int>`：**8 字节**，只有一个对象指针（默认删除器不占空间）。
- `shared_ptr<int>`：**16 字节**，对象指针 + 控制块指针。
- 控制块另外在堆上，含强/弱计数、删除器；`make_shared` 时对象与控制块同一块分配。
