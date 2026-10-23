---
id: hl-c11-memcpy-memmove-diff
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 8
---
## Q
面试问：`memcpy` 和 `memmove` 的区别？
Interview question: What is the difference between `memcpy` and `memmove`?

## A
- 区别只在**重叠**：`memmove` 对重叠区域定义良好（要么选择拷贝方向，要么用临时缓冲）；`memcpy` 假设不重叠，重叠是 UB。
- 正因为假设不重叠，`memcpy` 实现可以更激进（并行、向量化）；`memmove` 略多一次重叠判断。
- 两者单位都是字节，都不做类型检查。
