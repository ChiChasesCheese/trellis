---
id: hl-c04-copy-elision
node: cpp-lessons.c04-move-semantics
type: qa
step: 13
---
## Q
什么是复制省略（copy elision）？C++17 保证省略和 NRVO（具名返回值优化）有什么区别？

## A
编译器直接把对象构造在最终位置，**根本不调用拷贝/移动构造**。
- **C++17 保证省略**：用纯右值（`return Pinned(7);`、`Heavy h = make();`）初始化对象时不存在临时对象，所以连**不可拷贝也不可移动**的类型也能这样返回。
- **NRVO**：返回具名局部变量 `h`，编译器通常直接把 `h` 构造在调用者的位置；**允许但不保证**。
- 当两个不同局部变量都可能被返回时，无法 NRVO，但 `return a;` 会自动按右值处理（隐式移动）。
- 实测：`return Heavy("prvalue");` 只有一次 `ctor`；`return h;` 同样只有一次 `ctor`。
