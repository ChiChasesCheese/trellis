---
id: hl-cx-floorlog2-code
node: foundations.complexity
type: qa
step: 20
---
## Q
用 Java 写出 `floorLog2(long n)`：先用循环实现，再给出用 `Long.numberOfLeadingZeros` 的内置写法。

## A
```java
static int floorLog2(long n) {
    int k = 0;
    while (n > 1) { n >>= 1; k++; }   // 折半几次到 1
    return k;
}
static int floorLog2Fast(long n) {
    return 63 - Long.numberOfLeadingZeros(n);
}
```
循环版 O(log n)；内置版是前导零个数，O(1)，通常对应一条 CPU 指令。
