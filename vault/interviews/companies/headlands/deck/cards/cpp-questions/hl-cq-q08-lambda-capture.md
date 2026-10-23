---
id: hl-cq-q08-lambda-capture
node: cpp-questions.b-standards
type: qa
step: 11
---
## Q
C++ lambda 的捕获列表 `[x]`、`[&x]`、`[=]`、`[&]` 分别是什么意思？最常见的陷阱是什么？

## A
- `[x]`：按值（拷贝）捕获 `x`。
- `[&x]`：按引用捕获 `x`。
- `[=]` / `[&]`：把用到的变量全部按值 / 全部按引用捕获。
- 陷阱：按引用捕获的局部变量，在 lambda 比它**活得久**时会成为**悬空引用**（dangling reference）。
