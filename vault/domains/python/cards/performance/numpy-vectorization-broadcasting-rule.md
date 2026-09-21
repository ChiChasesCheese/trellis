---
id: numpy-vectorization-broadcasting-rule
node: performance.numpy-vectorization
type: qa
tags: [grown]
---
## Q
NumPy 的广播（broadcasting）机制在什么条件下允许两个不同形状的数组直接做逐元素运算？广播过程中会真的把小数组复制成大数组吗？

## A
从末尾维度开始逐维比较两个数组的形状：每一维要么相等，要么其中一个是 1，否则维度数不够时把缺的维度当作 1；只要每一维都满足这个条件就能广播，否则报形状不匹配的错误。广播不会真的分配内存把小数组复制成大数组，而是在那一维上把步长（stride）当作 0，让计算时反复读取同一份数据，不产生额外拷贝。
