---
id: numpy-vectorization-push-to-c
node: performance.numpy-vectorization
type: qa
tags: [grown]
---
## Q
NumPy 的向量化（vectorization）操作，比如 `a + b`（两个 `ndarray` 相加），为什么比写一个 Python 层的 `for` 循环逐元素相加要快？

## A
向量化把逐元素的循环从 Python 解释器下推到用 C 实现的批量遍历里执行：C 循环不需要每次迭代都走 Python 字节码分发、动态类型检查、以及把结果重新装箱成 Python 对象，而是直接在一段连续内存上按固定步长做同一种机器指令操作，省掉了 Python 解释器逐次调度的固定开销。
