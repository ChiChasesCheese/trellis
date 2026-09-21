---
id: numpy-vectorization-order-of-magnitude
node: performance.numpy-vectorization
type: qa
tags: [grown]
---
## Q
对可向量化的数值计算，NumPy 向量化写法相对等价的纯 Python `for` 循环，速度差距大致在什么量级？

## A
量级上通常快一到两个数量级（即几十倍到上百倍），具体倍数取决于数组大小、元素类型和操作复杂度；差距的来源主要是省掉了 Python 解释器逐元素调度的固定开销，而不是 CPU 算力本身有数量级差异。
