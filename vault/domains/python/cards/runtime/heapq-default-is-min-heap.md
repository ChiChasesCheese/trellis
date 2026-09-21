---
id: heapq-default-is-min-heap
node: runtime.stdlib-map
type: qa
source: python-docs
---
## Q
`heapq` 模块默认实现的是小顶堆还是大顶堆？怎么知道堆顶元素是谁？想要「取最大值」的语义怎么办？

## A
`heapq` 默认实现小顶堆（min-heap）：只要一个列表满足 `heap[k] <= heap[2k+1]` 且 `heap[k] <= heap[2k+2]`（下标从 0 开始），堆顶 `heap[0]` 就一定是最小元素。想要大顶堆语义，要么把存入的值取负号，要么用名字带 `_max` 后缀的那组函数（如 `heapify_max()`），它们维护相反的不变式，这时 `heap[0]` 是最大元素。
