---
id: hl-j15-intermediate-overflow
node: java21.j15-math-string-utils
type: qa
step: 18
---
## Q
`Math.addExact` 抛了 `ArithmeticException`，是不是说明最终结果一定装不下？该怎么应对？

## A
不是。`addExact(a, b)` 在 `a + b` 超出时抛异常，**即便最终结果（后面还要减回去）能装下**。例：求 `Long.MIN_VALUE..Long.MAX_VALUE` 的和，结果恰是合法的 `Long.MIN_VALUE`，但中间量会溢出。

应对：捕获 `ArithmeticException`，退到 `BigInteger` 算精确值再判断能否装下。也可以改变运算顺序，如先除 2 再乘，少一次溢出机会。

**抛异常不等于「错」，只是「这条快路径不能下结论」。**
