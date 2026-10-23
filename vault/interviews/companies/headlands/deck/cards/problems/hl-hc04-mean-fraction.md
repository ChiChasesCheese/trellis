---
id: hl-hc04-mean-fraction
node: problems.hc04-queue-mean-snapshot
type: qa
step: 7
---
## Q
精确均值为什么返回约分分数 `Mean`？紧凑构造器里怎么约分？`getMean()` 的快路径是什么？

## A
均值 = 总和 / 个数是分数。`6/4` 和 `3/2` 是同一个数，约成最简、**分母恒为正、符号放分子**，`record` 的 `equals` 才可直接比较（`6/-4` 与 `-3/2` 不约分就不相等）。`double` 已经舍入，不能精确比较。

```java
public record Mean(BigInteger numerator, long denominator) {
    public Mean {
        if (denominator <= 0) throw new IllegalArgumentException(...);
        BigInteger g = numerator.gcd(BigInteger.valueOf(denominator));
        if (g.signum() != 0 && !g.equals(BigInteger.ONE)) {
            numerator = numerator.divide(g);
            denominator /= g.longValueExact();
        }
    }
}
```
紧凑构造器**重新赋值参数**就是约分，所以 `new Mean(6, 4)` 得 `3/2`。分子为 0 时 `gcd(0, d) = d`，得 `0/1`。`BigInteger` 不溢出但每次分配新对象，所以只在**取答案**时用，不在每次 push/pop 里用。

**`getMean()` 快路径**：
```java
if (hi == (lo >> 63) && lo >= -(1L << 53) && lo <= (1L << 53)) return (double) lo / size;
return mean().toDouble();
```
和在 ±2⁵³ 内时分子和 `size` 都能精确表示成 `double`，一次 IEEE 除法就是正确舍入，不分配；否则走 `BigDecimal` 慢路径。

渲染：整数 `7`、分数 `-7/2`、空队列 `empty`。
