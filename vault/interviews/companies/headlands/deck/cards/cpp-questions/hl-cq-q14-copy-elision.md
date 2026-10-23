---
id: hl-cq-q14-copy-elision
node: cpp-questions.c-memory-ownership
type: qa
step: 22
---
## Q
C++17 的“保证的复制省略”和命名返回值优化（NRVO）有什么区别？既不可拷贝也不可移动的类型能按值返回吗？

## A
- **返回 prvalue（临时对象）**：C++17 起**保证**直接构造在调用者的位置，实测 `ctor=1 copy=0 move=0`。
- **返回具名局部变量（NRVO）**：编译器**允许但不保证**省略，clang 做了（同样 `ctor=1 copy=0 move=0`）。
- 既不可拷贝也不可移动的类型（如 `Pinned`）也能从函数里按值返回临时对象，因为根本没有拷贝或移动发生。
- 因此 `return std::move(x)` 反而会阻止省略，编译器会警告。
