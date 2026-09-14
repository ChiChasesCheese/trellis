---
id: vectorized-vs-row-at-a-time
node: query.vectorized-columnar-execution
type: qa
tags: [grown]
---
## Q
对 10 亿行做 `SUM(price * qty)`，为什么按批次、面向列的向量化执行远快于逐行解释执行（tuple-at-a-time）？

## A
逐行解释执行对每一行都要走一遍通用的算子调用、类型分派和表达式解释，这些控制开销乘以 10 亿次，远超真正的乘法与加法。向量化执行把这些开销摊到每批几千行上：对 price 和 qty 两个连续数组做紧密循环，数据在内存中连续，CPU 缓存命中率高，编译器和 CPU 也能使用 SIMD（单指令多数据）指令一次处理多个值。并且只需读取和处理用到的两列。
