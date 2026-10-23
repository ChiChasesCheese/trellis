---
id: hl-j15-overflow-basics
node: java21.j15-math-string-utils
type: qa
step: 1
---
## Q
Java 的 `int`、`long` 范围是多少？整数溢出（overflow）是什么？为什么在交易里是最糟的 bug？

## A
整数是固定宽度二进制，最高位当符号位（补码，two's complement）：
- `int` 32 位：−2 147 483 648 ~ 2 147 483 647（约 ±21 亿）；
- `long` 64 位：−9 223 372 036 854 775 808 ~ 9 223 372 036 854 775 807（约 9.2×10¹⁸）。

超出范围**不会报错**，像里程表一样绕回去：`Integer.MAX_VALUE + 1` 变成 `Integer.MIN_VALUE`。

交易里价格用最小价位的整数倍（tick）存成 `long`，数量也是 `long`，名义金额 = 价格 × 数量：价格 4×10⁹ tick、数量 3×10⁹ 就超过 9.2×10¹⁸。静默回绕的后果不是崩溃，而是**一个看起来正常的错误数字**，甚至负的成交额。
