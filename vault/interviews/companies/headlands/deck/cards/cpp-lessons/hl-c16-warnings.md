---
id: hl-c16-warnings
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 12
---
## Q
本地开发用 `-Wall -Wextra` 时，`-Wsign-compare`、`-Wunused-variable`、`-Wreturn-type`、`-Wsometimes-uninitialized` 各对应什么问题？

## A
- `-Wsign-compare`：`int` 与 `size_t` 比较（`for (int i = 0; i < v.size(); ++i)`）。
- `-Wunused-variable`：声明了没用的变量。
- `-Wreturn-type`：非 void 函数在某些路径上没有 `return`，**走到末尾是 UB**。
- `-Wsometimes-uninitialized`：变量在某个分支下没赋值就被读取（读未初始化变量）。

CoderPad 一般看不到警告，但本地每个警告都值得处理，它们常指向真 bug。
