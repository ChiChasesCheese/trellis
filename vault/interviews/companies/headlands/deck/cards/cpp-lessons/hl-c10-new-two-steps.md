---
id: hl-c10-new-two-steps
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 5
---
## Q
`new T(args)` 实际分成哪两步？`operator new` 能自定义吗？

## A
- 第一步：`operator new(sizeof(T))` 取原始内存；第二步：在那块内存上调用构造函数。
- `operator new` 是普通的**可替换函数**：可全局替换，也可为某个类重载，常用于统计、池化、调试。
- 例：测试里替换全局 `operator new`，对超大请求直接 `throw std::bad_alloc()`，来模拟内存耗尽。
- placement new 只做第二步。
