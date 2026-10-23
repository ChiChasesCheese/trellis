---
id: hl-j04-version-and-bits
node: java21.j04-record-patterns
type: qa
step: 27
---
## Q
record 模式在哪个 Java 版本正式？Pair 的 `Bit` 有 `Zero`、`One` 两个实现时，穷尽的 `switch` 至少要几个 `case`？

## A
- 版本：**Java 21 正式**（19、20 为预览）。
- `Pair(Bit a, Bit b)` 要覆盖 2 × 2 = **4** 个组合：`(Zero,Zero)`、`(Zero,One)`、`(One,Zero)`、`(One,One)`。
- 除非用无条件子模式 `Pair(Bit a, Bit b)` 合并成一个 `case`。
