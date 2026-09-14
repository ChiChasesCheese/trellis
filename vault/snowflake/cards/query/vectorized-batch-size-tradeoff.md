---
id: vectorized-batch-size-tradeoff
node: query.vectorized-columnar-execution
type: qa
tags: [grown]
---
## Q
向量化执行（vectorized execution）为什么选择“每批几千行”，而不是每批 1 行或一次处理整列全部数据？

## A
每批 1 行就退化回逐行执行，控制开销无法摊薄。一次处理整列全部数据则中间结果太大，放不进 CPU 缓存，还要把整个中间结果完整物化在内存里，内存压力大、无法流水线传递。几千行是折中：批次足够大，能摊薄每批的调度开销；又足够小，一批的列数组能留在 CPU 缓存中，并在算子之间流式传递。
