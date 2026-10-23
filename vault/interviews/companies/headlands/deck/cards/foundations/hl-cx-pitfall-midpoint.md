---
id: hl-cx-pitfall-midpoint
node: foundations.complexity
type: qa
step: 37
---
## Q
二分查找里为什么不能写 `(lo + hi) / 2` 求中点？正确写法有哪两种？

## A
`lo + hi` 超过 `Integer.MAX_VALUE`（约 21 亿）时会溢出成负数，导致下标越界。这个 bug 在 JDK 的 `Arrays.binarySearch` 里真实存在多年（2006 年发现并修复）。

正确写法：
```java
int mid = lo + (hi - lo) / 2;
int mid2 = (lo + hi) >>> 1;   // 无符号右移，加法溢出了符号位结果也正确
```
