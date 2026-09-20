---
nodes: [problems.search.metrics-monitoring]
url: https://prometheus.io/docs/prometheus/latest/storage/
---
# Prometheus – Storage

值得读：Prometheus 官方文档，第一方来源，披露了默认 2 小时块时长、128MB 的 WAL 段大小、
压缩块最终可以合并到保留期 10%（或 31 天，取更小值）的时间跨度、以及"平均 1–2 字节/样本"
的经验数字。本题解「深入探讨」第 2 节的内存头块窗口设计对齐了这份文档的默认块时长，但
没有照搬它给出的"1–2 字节/样本"经验值，而是用自己实现的 Gorilla 式压缩算法在三种合成场景
上重新计算，得到一个范围（约 0.7–7.1 字节/样本）而不是单一常数——因为真实压缩比强烈依赖
指标本身的变化模式，一个笼统的经验值不足以支撑容量估算。
