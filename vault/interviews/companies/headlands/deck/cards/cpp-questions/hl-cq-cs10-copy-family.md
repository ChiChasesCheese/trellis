---
id: hl-cq-cs10-copy-family
node: cpp-questions.cheatsheet
type: qa
step: 10
---
## Q
一句话背诵：`std::copy`、`memcpy`、`memmove` 的规则，`pair<int,int>` 是否 trivially copyable，类型双关用什么？

## A
- `memcpy`：复制字节，重叠是 UB，仅限 trivially copyable。
- `memmove`：允许重叠。
- `std::copy`：类型感知，对 `int` 数组就编译成一次 `memmove`。
- `std::pair<int,int>` **不是** trivially copyable。
- 类型双关用 `std::bit_cast`。
