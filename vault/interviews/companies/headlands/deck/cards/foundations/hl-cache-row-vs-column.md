---
id: hl-cache-row-vs-column
node: foundations.cpu-cache-locality
type: qa
step: 11
---
## Q
遍历 Java 的 `int[4096][4096]`，行优先（row-major）和列优先（column-major）都是 O(n²) 加法，为什么列优先慢约 7.7 倍？写出两种循环。

## A
Java 的二维数组是「行的数组」：每一行是一个连续的 `int[4096]`（16 KB），行与行是不同对象。

```java
for (int i = 0; i < n; i++)      // 行优先：内层连续
    for (int j = 0; j < n; j++) s += m[i][j];
for (int j = 0; j < n; j++)      // 列优先：内层跳 16 KB
    for (int i = 0; i < n; i++) s += m[i][j];
```
实测 3.56 ms 对 27.37 ms（多次运行 6–9 倍）。列优先每次访问跳过 16 KB，等于每次读一个新缓存行，只用其中 4 字节，其余 124 字节白搬了。

法则：嵌套循环里，**让最内层循环的下标对应内存中连续变化的那一维**。
