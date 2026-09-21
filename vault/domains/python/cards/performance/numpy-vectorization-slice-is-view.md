---
id: numpy-vectorization-slice-is-view
node: performance.numpy-vectorization
type: qa
tags: [grown]
---
## Q
对 `ndarray` 做基本切片（如 `a[1:4]`）得到的是原数组的拷贝还是视图（view）？这和对 Python `list` 做切片的行为有什么不同，容易踩什么坑？

## A
基本切片返回的是视图，和原数组共享同一块底层内存，修改切片元素会直接改到原数组上；这和 `list` 切片总是分配新列表、互不影响不同。常见的坑是以为切片结果和原数组无关就随手修改，结果污染了原数组，需要显式调用 `.copy()` 才能得到真正独立的副本。
