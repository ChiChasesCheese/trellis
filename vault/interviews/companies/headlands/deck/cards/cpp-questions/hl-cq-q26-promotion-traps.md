---
id: hl-cq-q26-promotion-traps
node: cpp-questions.f-ub-debug
type: qa
step: 18
---
## Q
`~uint8_t(0x0F)` 的值和类型是什么？怎么得到 `0xF0`？有符号数 `-16 >> 2` 是多少？`1u << 31`、`1 << 31`、`sizeof(1 << 3)` 和 `sizeof(1LL << 40)` 各说明什么？

## A
- `~uint8_t(0x0F)`：`uint8_t` 先**提升成 `int`**，结果是 `int` -16（0xFFFFFFF0），大小 4 字节，不是 0xF0。要截回去必须显式转换：`(uint8_t)~b = 240`。
- 用 `cout` 打印 `uint8_t` 会当成 `char` 输出；用 `printf` 要写 `%u`。
- 有符号右移是**算术右移**：`-16 >> 2 = -4`；转成无符号再移是 1073741820。
- `1u << 31 = 2147483648`；`1 << 31` 会移进 `int` 的符号位。
- 字面量 `1` 是 `int`（`sizeof(1 << 3)=4`），要移位 ≥ 32 位必须写 `1ULL`（`sizeof(1LL << 40)=8`）。
