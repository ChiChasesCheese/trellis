---
id: hl-fit-d3-performance
node: company.fit
type: qa
step: 15
---
## Q
JD 日常工作 "Address performance limitations within our own software, open-source libraries and applications, Linux, etc."，你的最接近故事是什么？讲的时候要划清哪条边界？

## A
评级：**部分（偏弱）**，也是**最大的单项缺口**。

- 简历没有性能 bullet。最接近的故事：识别"逐行 numpy 推理在 7.6 亿行 / 天规模下会超时"，把上线拆成两阶段：先上纯 SQL pushdown 的确定性规则，模型推理放到 go/no-go 门后。
- 这是**设计期推理，不是剖析（profiling）出来的**。要说清："this was capacity reasoning before anything shipped, not profiling a running system."
- Quant-Stroller 没有向量化也没有基准数字，**不要说成性能成果**。
- 要补：缓存局部性；JIT / GC；Linux 工具；找一个真实排查案例。
