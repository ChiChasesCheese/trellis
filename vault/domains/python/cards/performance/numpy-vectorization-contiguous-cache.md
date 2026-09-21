---
id: numpy-vectorization-contiguous-cache
node: performance.numpy-vectorization
type: qa
tags: [grown]
---
## Q
`ndarray` 把同类型元素存成一段连续内存（contiguous memory），这对 CPU 缓存（cache）意味着什么？和存一堆 Python 对象引用的 `list` 相比差别在哪？

## A
连续内存里相邻元素在物理地址上也相邻，CPU 按固定步长（stride）访问时，缓存预取（prefetch）能一次性把后面要用的元素也拉进缓存，命中率高；`list` 存的是指向各个 Python 对象的指针，对象本身分散在堆的不同位置，遍历时经常要跳到缓存之外的地址，缓存不命中（cache miss）的概率更高。
