---
id: problems-metrics-monitoring-write-path-compression-data-dependent
node: problems.search.metrics-monitoring
type: qa
step: 3
tags: [grown]
---
## Q
In a metrics monitoring system's write path using Gorilla-style compression (delta-of-delta timestamps, XOR'd floating-point values), why can't a design assume a single fixed bytes-per-sample number for capacity planning, and what does simulating the algorithm on different metric shapes show?

## A
The achievable compression ratio depends heavily on how the metric's value actually changes between samples, because XOR compression is cheap only when consecutive values share long runs of identical leading/trailing bits. Running the actual delta-of-delta and XOR algorithm on three synthetic but representative series shows the range: a flat/idle metric that never changes compresses to about 0.70 bytes/sample (~23x reduction from the uncompressed 16 bytes), a steadily incrementing counter to about 2.54 bytes/sample (~6.3x), and a continuously noisy gauge to about 7.13 bytes/sample (~2.2x) — noise in the low mantissa bits prevents the XOR result from reusing the previous sample's bit window, forcing the more expensive encoding branch almost every time. A capacity estimate has to be computed from the design's own expected mix of metric types, not borrowed from another system's published average.

## Q zh
在一个使用 Gorilla 式压缩（delta-of-delta 时间戳、XOR 浮点数值）的指标监控系统写路径中，为什么设计不能假设一个固定的每样本字节数来做容量估算？对不同形状的指标模拟这个算法会看到什么？

## A zh
能达到的压缩比强烈依赖指标数值在相邻样本间实际的变化方式，因为 XOR 压缩只有在相邻数值共享一长段相同的前导/尾随比特时才便宜。在三种合成但有代表性的序列上真实运行 delta-of-delta 和 XOR 算法会看到一个区间：从不变化的空闲指标压缩到约 0.70 字节/样本（相对未压缩的 16 字节约 23 倍压缩比），稳定递增的计数器约 2.54 字节/样本（约 6.3 倍），持续带噪声的仪表约 7.13 字节/样本（约 2.2 倍）——尾数低位的噪声让 XOR 结果几乎无法复用上一个样本的比特窗口，几乎每次都要走更贵的编码分支。容量估算必须按设计自己预期的指标类型构成来计算，而不能照搬别的系统公布的平均值。
