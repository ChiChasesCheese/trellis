---
id: hl-cq-q26-script
node: cpp-questions.f-ub-debug
type: qa
step: 22
---
## Q
用英文 60 秒回答：Bitwise operations on a register: set, clear, toggle, test, shifts, rotate, popcount. What are the traps?

## A
结构：无符号定宽类型，置位/清位/翻转/测试与 `<bit>` → 陷阱：移位 ≥ 位宽是 UB、`uint8_t` 提升、有符号右移、`==` 优先级、`1u` → 小技巧 `x & (x-1)`、`x & -x`。

- I use **unsigned fixed-width** types and unsigned literals. Set is OR with a mask, clear is AND with the **inverted** mask, toggle is XOR, test is shift-then-AND-one. Rotate is `(r << n) | (r >> (32 - n))` with `n` masked and the zero case handled, or `std::rotl` in C++20; `std::popcount`, `countr_zero` and `countl_zero` are in `<bit>`.
- The traps I check first: **shifting by the width or more is undefined** so I guard it; `uint8_t` values are **promoted to int** so `~b` is a negative int; right shift of a **signed** value is arithmetic; precedence - `==` binds tighter than `&`, so I parenthesize; and `1 << 31` lands in the sign bit, so I write `1u`.
- Tricks: `x & (x-1)` clears the lowest set bit, `x & -x` isolates it, and a power of two test is `x && !(x & (x-1))`.
