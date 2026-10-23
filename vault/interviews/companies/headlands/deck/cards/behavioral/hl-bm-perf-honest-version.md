---
id: hl-bm-perf-honest-version
node: behavioral.method
type: qa
step: 17
---
## Q
被问 "讲一个你优化过的性能问题" 而你没有真正剖析（profiling）过的故事时，诚实版怎么答？什么话绝对不能说？

## A
**不能说**："I optimized it and it ran 10x faster."（没有这样的故事。）

**能说**（先把边界摆出来）：
- "The honest version is **capacity reasoning rather than profiling**."
- 继承的异常检测器只在 **6 个合成商户**上跑过；生产约 **18,000 商户**、峰值一天最多约 **7.6 亿行**。
- 逐行 Python 推理的成本是 **每行成本 × 峰值行数**，QA 永远显示不出来。
- 我提议第一阶段把确定性规则做成仓库内的**集合式 SQL**（set-based），模型部分放在**go/no-go 门**后面。
- "If it had been running, I'd have measured per-row latency at small scale and checked how much is data movement first."

先说"这不是剖析"，面试官记下的是"诚实、会算规模"。
