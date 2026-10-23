---
id: hl-hc03-range-sum
node: problems.hc03-recursive-sum
type: qa
step: 12
---
## Q
区间 `[a, b]`（可为负）求和 `rangeSum` 怎么写？为什么「中间量溢出 ≠ 结果溢出」，快路径失败后怎么办？

## A
```java
long s = Math.addExact(a, b);
long count = Math.addExact(Math.subtractExact(b, a), 1);
long v = (count & 1) == 0 ? Math.multiplyExact(count / 2, s)
                          : Math.multiplyExact(count, s / 2);
return new Ok(v);
// 任何一步抛 ArithmeticException：
var exact = rangeSumExact(a, b);                 // BigInteger
return exact.bitLength() <= 63 ? new Ok(exact.longValueExact()) : new Overflow(exact);
```
- `a > b` 抛 `IllegalArgumentException`（约定，面试先问清楚）；`count` 为偶则 `s` 必为奇，故除 `count`，反之除 `s`。
- `a+b` 和 `b−a+1` 自己会溢出：`a=MIN, b=MAX` 时 `b−a+1 = 2⁶⁴`；`a=b=MAX` 时 `a+b` 溢出。
- 但**中间量溢出不等于结果溢出**：`MIN..MAX` 的和除 `MIN` 外两两抵消，剩 `Long.MIN_VALUE`，装得下 → `Ok(Long.MIN_VALUE)`；`MAX..MAX` 的和就是 `MAX`。
- 所以快路径用 `addExact/subtractExact/multiplyExact`，任何一步抛异常就**退到 `BigInteger`** 算精确值，再用 `bitLength() <= 63`（不含符号位，−2⁶³..2⁶³−1 都满足）判断装不装得下。`BigInteger` 是慢但永远正确的备选，也用来验证快速实现；`shiftRight(1)` 是除以 2。
- 快路径无分配，O(1)。
