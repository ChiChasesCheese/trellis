---
id: hl-cq-q23-script
node: cpp-questions.f-ub-debug
type: qa
step: 4
---
## Q
用英文 60 秒回答：What is undefined behavior? Why does C++ have it? Give examples.

## A
结构：定义（标准无要求，编译器可假设不发生）与存在理由 → 例子清单 → `x + 1 > x`（`-O0` 假、`-O2` 真）与无符号回绕 → 用 UBSan/ASan 抓、溢出内建函数。

- **Undefined behavior** means the standard places no requirements on the program, so the compiler may assume it never happens and optimize on that assumption. C++ has it so that checks - bounds, overflow, null - cost nothing unless I ask for them.
- Examples: signed overflow, out-of-bounds access, dangling pointers, reading uninitialized memory, shifting by the width or more, data races, and falling off the end of a non-void function.
- A concrete case: `x + 1 > x` for a signed int. At `-O0` with `INT_MAX` it returns false because it wrapped; at `-O2` it returns **true** because the compiler folded it to a constant. Unsigned overflow is defined and wraps.
- I catch these with **UBSan** and **ASan**, and use `__builtin_add_overflow` when I need checked arithmetic.
