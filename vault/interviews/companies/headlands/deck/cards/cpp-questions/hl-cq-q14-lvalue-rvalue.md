---
id: hl-cq-q14-lvalue-rvalue
node: cpp-questions.c-memory-ownership
type: qa
step: 23
---
## Q
C++ 的左值、右值是怎么区分的？类型是 `T&&` 的函数参数在函数体里算左值还是右值？怎么让它再变成右值？

## A
- **右值**（rvalue）：临时的、没有名字的东西。
- **有名字的变量是左值**，包括类型是 `T&&` 的参数。
- 要再次变成右值：用 `std::move`（无条件）或 `std::forward`（有条件）。
- 引用的三种形态：左值引用 `T&`、右值引用 `T&&`、值。
