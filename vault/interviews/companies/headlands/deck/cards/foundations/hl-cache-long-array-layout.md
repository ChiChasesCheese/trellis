---
id: hl-cache-long-array-layout
node: foundations.cpu-cache-locality
type: qa
step: 13
---
## Q
`long[] a = new long[4]` 在 JVM 内存里怎么布局？10⁷ 个 `long` 占多少，每元素实测多少字节？

## A
一整块连续内存：16 字节对象头（8 B mark word + 4 B klass 指针 + 4 B 数组长度），后面是 4 × 8 = 32 字节数据。每个 `long` 占 8 字节，整个数组共享一个 16 字节头。

10⁷ 个 `long` ≈ **80 MB**；实测每元素 **8.2 字节**（多出的 0.2 是测量噪声）。
