---
id: hl-c02-param-choice
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 3
---
## Q
C++ 函数参数类型怎么选？覆盖：廉价小类型、只读大对象、要修改调用者对象、要取得所有权。

## A
日常 90% 的决策：
- **小的、廉价可拷贝的类型**（`int`、`double`、指针、`string_view`、`span`）：按**值**。
- **只读大对象**：`const T&`。
- **要修改调用者的对象**：`T&`；如果"可以没有"，用指针。
- **要取得所有权或存下来**：按值接收后 `std::move` 进成员（`std::move` 把对象标记为"可以被偷走资源"），或用 `unique_ptr<T>`（独占所有权的智能指针）。

例：`void f(const std::vector<int> v)` 是错误写法：按值传会复制整个 vector，而 `const` 只约束函数内部；应写 `const std::vector<int>&`。
