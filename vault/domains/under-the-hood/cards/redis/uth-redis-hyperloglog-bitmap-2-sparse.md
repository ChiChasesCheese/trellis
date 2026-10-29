---
id: uth-redis-hyperloglog-bitmap-2-sparse
node: redis.hyperloglog-bitmap
type: qa
step: 2
---
## Q
**HyperLogLog 刚创建时有多大**｜Redis · HyperLogLog

只加了几百个元素的 HLL，也要占 12KB 吗？

## A
**结构。** 不用，先用稀疏编码（sparse）：对寄存器做游程编码（run-length encoding）。

**细节。**

- 三种操作码：`ZERO`（连续 1 到 64 个 0）、`XZERO`（最多 16384 个 0）、`VAL`（值 1 到 32，重复 1 到 4 次）
- 空的 HLL 就是一条 `XZERO:16384`
- 平均占用：100 个元素约 267 字节，1000 个约 1882，10000 个约 10591
- 超过 `hll-sparse-max-bytes`（默认 3000）或寄存器值大于 32，转成稠密编码

**为什么。** 小基数时绝大多数寄存器还是 0，压缩划算；基数大了，稀疏的读写开销不值得。

**对应 LeetCode：** LC 443 压缩字符串 · LC 38 外观数列
