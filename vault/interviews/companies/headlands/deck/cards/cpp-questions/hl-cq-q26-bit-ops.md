---
id: hl-cq-q26-bit-ops
node: cpp-questions.f-ub-debug
type: qa
step: 17
---
## Q
面试题：对一个寄存器值做位运算——置位、清位、翻转、测试、移位、循环移位、popcount——怎么写？有哪些陷阱？
Bitwise operations on a register: set, clear, toggle, test, shifts, rotate, popcount. What are the traps?

## A
用**无符号**类型（`uint32_t`）和**无符号常量**（`1u << b`）：
- 置位 `r | mask`
- 清位 `r & ~mask`
- 翻转 `r ^ mask`
- 测试 `(r >> b) & 1`
- 位移量必须小于类型位宽；小于 `int` 的类型运算前会先**提升**成 `int`。
- C++20 `<bit>`：`std::popcount`、`std::countr_zero`（ctz）、`std::countl_zero`（clz）、`std::rotl` / `std::rotr`、`std::bit_ceil`、`std::has_single_bit`。
- 循环移位的手写形式是 `(r << n) | (r >> (32 - n))`，要把 `n` 取模并处理 0 的情况。
