---
id: hl-cq-q26-bit-tricks
node: cpp-questions.f-ub-debug
type: qa
step: 20
---
## Q
位运算的三个常用技巧：`x & (x-1)`、`x & -x`、判断 2 的幂，各做什么、怎么写？

## A
- `x & (x-1)`：清掉**最低位的 1**。
- `x & -x`：**取出最低位的 1**（isolate the lowest set bit）。
- 2 的幂测试：`x && !(x & (x-1))`；C++20 可用 `std::has_single_bit`。
- 对应还有 Kernighan 循环：每次 `x &= x-1` 数 1 的个数，复杂度是 1 的个数。
