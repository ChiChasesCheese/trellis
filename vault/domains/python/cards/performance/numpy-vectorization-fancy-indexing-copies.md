---
id: numpy-vectorization-fancy-indexing-copies
node: performance.numpy-vectorization
type: qa
tags: [grown]
---
## Q
用整数数组或布尔数组做索引（花式索引，fancy indexing），比如 `a[a > 0]`，得到的结果是视图还是拷贝？为什么容易和切片视图的直觉搞混？

## A
花式索引总是返回一份拷贝，而不是像基本切片那样共享内存。容易踩的坑是：写惯了 `a[1:4][:] = 0` 能就地修改原数组，就以为 `a[mask][:] = 0` 也能修改原数组，实际上 `a[mask]` 已经是独立拷贝，改它对原数组毫无影响，要就地修改必须写成 `a[mask] = 0`。
