---
id: hl-bm-t2-fallback
node: behavioral.method
type: qa
step: 31
---
## Q
在真实性能排查故事还没补上之前，被问性能经历时的替代答法是什么？为什么另外两个故事也不能冒充剖析？

## A
替代答法：先说 **"my clearest example is capacity reasoning, not profiling"**，讲 S6（上线前用规模估算叫停逐行方案），再讲**你会怎么剖析**（先量每行延迟、分开 CPU 与数据搬运、外推）。

为什么不能冒充剖析：
- S6 是**上线前的容量推理**，系统从未在规模上运行过。
- S5 的窗口化 `ON` 是**设计推理**（凭聚簇方式估计剪枝有效），没有读过 partitions scanned 的前后对比。

把推理说成测量，被追问一次就会露出来。
