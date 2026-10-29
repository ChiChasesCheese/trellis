---
id: tlc-maximum-lcci-3-why
node: b.maximum-lcci
type: qa
step: 3
---
## Q
**面试题 16.07 最大数值**｜正确性

为什么 `(diff >> diff.bit_length()) & 1` 能当作「`a < b`」的开关？写成固定的 `diff >> 31` 会在什么输入上出错？

## A
**不变量。** 设 `d = diff`，`d.bit_length()` 是表示 `|d|` 所需的位数，所以 `|d| < 2^bit_length`。

- `d >= 0`：`d >> bit_length` 把所有有效位都移出去，结果是 `0`。
- `d < 0`：Python 的右移是算术右移（补符号位 1），`d` 在 `-2^bit_length < d < 0`，结果是 `-1`，其二进制全是 1，`& 1` 得 `1`。

所以 `neg` 恰好是「`a < b`」的 0/1 值，`a - neg * diff` 在两种情况下分别得到 `a` 和 `b`。

**反例。** 固定 `diff >> 31`（只适合 `diff` 落在 32 位范围内）：`a = 2147483647`，`b = -1`，`diff = 2147483648 = 2^31`，`diff >> 31 = 1`，被当成负数，返回 `b = -1`；正确是 `2147483647`。`bit_length` 版本得到 `2147483647`。
