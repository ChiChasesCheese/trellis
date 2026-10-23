---
id: hl-heap-qa-peek-poll
node: foundations.heap-priority-queue
type: qa
step: 32
---
## Q
追问：为什么 `PriorityQueue` 的 `poll` 是 O(log n)，`peek` 是 O(1)？

## A
推荐答法：「堆顶永远是最小元素，在数组下标 0，所以 `peek` 是 O(1)。`poll` 把末尾元素搬到根再下沉，路径长度是树高 log n，每层常数次比较，所以 O(log n)。」
