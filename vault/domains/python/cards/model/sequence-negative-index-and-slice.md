---
id: sequence-negative-index-and-slice
node: model.sequences
type: qa
source: python-docs
---
## Q
序列类型里，负数下标 `a[-2]` 等价于什么？带步长的扩展切片 `a[i:j:k]` 选出的是哪些下标的元素？

## A
对长度为 n 的序列，`a[-2]` 等价于 `a[n-2]`，即负数下标会先加上序列长度换算成非负下标。普通切片 `a[start:stop]` 选出满足 `start <= k < stop` 的所有下标 k；带步长的扩展切片 `a[i:j:k]` 选出所有满足 `x = i + n*k`（`n >= 0` 且 `i <= x < j`）的下标 x，即从 i 开始每隔 k 个取一个，直到小于 j 为止。切片位置越界不会报错，只是被截断到序列的有效范围内。
