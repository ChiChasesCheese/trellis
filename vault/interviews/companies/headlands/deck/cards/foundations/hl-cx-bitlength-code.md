---
id: hl-cx-bitlength-code
node: foundations.complexity
type: qa
step: 49
---
## Q
不用 `Math.log`，写一个函数数出正整数 n 的二进制位数，并说明复杂度和内置做法。

## A
```java
static int bitLength(long n) {
    int bits = 0;
    while (n > 0) { n >>= 1; bits++; }
    return bits;
}
```
每次右移一位相当于除以 2，共 ⌊log₂ n⌋ + 1 次，复杂度 **O(log n)**。内置做法 `64 - Long.numberOfLeadingZeros(n)` 是 O(1)（一条 CPU 指令）。
