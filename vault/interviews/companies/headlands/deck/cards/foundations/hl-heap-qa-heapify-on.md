---
id: hl-heap-qa-heapify-on
node: foundations.heap-priority-queue
type: qa
step: 33
---
## Q
追问：建堆为什么是 O(n)？

## A
推荐答法：「从最后一个非叶子节点倒着下沉。高度为 h 的节点最多 n/2^(h+1) 个，每个最多下沉 h 步，总和 Σ h·n/2^(h+1) = O(n)，因为 Σ h/2^h 收敛到 2。逐个插入是 O(n log n)。」
