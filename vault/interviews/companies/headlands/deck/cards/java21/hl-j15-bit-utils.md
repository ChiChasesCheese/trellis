---
id: hl-j15-bit-utils
node: java21.j15-math-string-utils
type: qa
step: 17
---
## Q
`Integer.bitCount(0b1011_0110)`、`numberOfTrailingZeros(0)`、`highestOneBit(100)`、`rotateLeft(0x80000001, 1)`、`reverseBytes(0x01020304)` 各是多少？

## A
- `bitCount(0b1011_0110) = 5`（置位个数）；
- `numberOfTrailingZeros(0) = 32`：约定是 int 位宽 32，**不是 -1**（`numberOfLeadingZeros(0)` 也是 32）；
- `highestOneBit(100) = 64`；
- `rotateLeft(0x80000001, 1) = 0x3`；
- `reverseBytes(0x01020304) = 0x04030201`。

用途：`(w << 6) + Long.numberOfTrailingZeros(word)` 在位图里找最低置位；容量是 2 的幂时 `numberOfTrailingZeros(capacity)` 就是 log₂。
