---
id: hl-c09-overflow-check
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 5
---
## Q
为什么 `bool overflows(int x) { return x + 1 < x; }` 不能检测 `int` 溢出？安全地检测溢出有哪几种写法？

## A
- 有符号溢出是 UB，编译器假定它不发生，`x + 1 < x` 被视为「永远为假」；`-O2` 下整个函数变成 `mov w0, #0; ret`，即 `return false`。对 `INT_MAX` 它也返回 false（溢出发生了，检查却说没有）。
- 安全写法：
  1. 先检查边界：`x == INT_MAX`。
  2. 用更宽类型（`long long`）。
  3. 编译器内建：`__builtin_add_overflow(a, b, &out)`（GCC/Clang），`INT_MAX + 1` 返回 true，结果回绕为 -2147483648。
- 无符号检查 `x + 1u < x` 是有效的，因为回绕有定义。
