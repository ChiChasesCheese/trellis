---
id: hl-hc03-twos-complement
node: problems.hc03-recursive-sum
type: qa
step: 3
---
## Q
补码（two's complement）怎样表示负数？`int` 和 `long` 的范围是多少？求和在 n 多大时溢出？

## A
补码里最高位的权重是**负的**。8 位权重：−128, 64, 32, 16, 8, 4, 2, 1。所以 `1111 1111` = −128 + 127 = −1，`1000 0000` = −128（最小数），`0111 1111` = 127（最大正数）。

溢出时硬件只保留低位，「绕回去」：127 + 1 = `1000 0000` = −128，**Java 整数加法不抛异常**，答案错了程序照常运行，最危险。

范围：`int` 32 位，−2³¹ ~ 2³¹−1 = −2 147 483 648 ~ 2 147 483 647；`long` 64 位，−2⁶³ ~ 2⁶³−1。

求和约 n²/2：`int` 在 **n = 65 536** 就装不下（1+…+65 535 = 2 147 450 880，再加 65 536 得 2 147 516 416，绕回 **−2 147 450 880**）；`long` 在 **n = 2³² = 4 294 967 296** 装不下。

精确运算：`Math.addExact` / `subtractExact` / `multiplyExact` / `negateExact` / `incrementExact`，溢出抛 `ArithmeticException`；`Math.toIntExact(long)` 装不下就抛。JIT 把 `addExact` 编译成一条加法加溢出标志检查，开销很小。C++ 里有符号溢出是 UB，不是回绕；无符号溢出才是定义良好的回绕（`UINT_MAX + 1 == 0`）。
