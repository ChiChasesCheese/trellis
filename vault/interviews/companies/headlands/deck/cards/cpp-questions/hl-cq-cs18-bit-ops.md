---
id: hl-cq-cs18-bit-ops
node: cpp-questions.cheatsheet
type: qa
step: 18
---
## Q
一句话背诵：位运算的写法和四个陷阱。

## A
- 置位 `r | (1u<<b)`，清位 `r & ~(1u<<b)`，翻转 `^`，测试 `(r>>b)&1`。
- `x & (x-1)` 清最低位，`x & -x` 取最低位；`std::popcount` / `rotl` / `countr_zero`。
- 坑：
  - 移位 ≥ 位宽是 UB；
  - `~uint8_t(0x0F)` 是 `int` **-16**；
  - 有符号右移是算术的；
  - `==` 优先级高于 `&`；掩码写 `1u`。
