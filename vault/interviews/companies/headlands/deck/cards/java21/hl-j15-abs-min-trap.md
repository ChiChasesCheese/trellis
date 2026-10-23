---
id: hl-j15-abs-min-trap
node: java21.j15-math-string-utils
type: qa
step: 4
---
## Q
`Math.abs(Long.MIN_VALUE)` 和 `Math.abs(Integer.MIN_VALUE)` 的结果是什么？为什么？用哪个方法才能暴露问题？

## A
结果**仍是负数**：`Math.abs(Long.MIN_VALUE) = -9223372036854775808`，`Math.abs(Integer.MIN_VALUE) = Integer.MIN_VALUE`。原因是 +9.2×10¹⁸（int 是 +2 147 483 648）超出该类型最大值，放不进去，补码绕回自己。

`Math.absExact` 才诚实：抛 `ArithmeticException: Overflow to represent absolute value of Long.MIN_VALUE`。同理 `negateExact(MIN)` 抛 `long overflow`。
