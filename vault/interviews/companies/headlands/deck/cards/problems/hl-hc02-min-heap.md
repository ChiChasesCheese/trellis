---
id: hl-hc02-min-heap
node: problems.hc02-merge-k-streams
type: qa
step: 3
---
## Q
最小堆（min-heap）怎么工作？为什么合并 k 路只用堆就能做到 O(N log k)？

## A
堆是完全二叉树，**每个节点都不大于它的两个孩子**，用数组存：下标 `i` 的父亲是 `(i-1)/2`，孩子是 `2i+1`、`2i+2`。
- `add`：放数组末尾，与父亲比，更小就交换，一路上浮（sift-up）；
- `poll`：取走根，把最后一个元素搬到根，与较小的孩子比，更大就交换，一路下沉（sift-down）。

每步只沿一条路径走，树高 log₂ n，所以都是 O(log n)。Java 的 `PriorityQueue` 就是最小堆，`poll()` 在空时返回 `null`；自定义比较器：`new PriorityQueue<>(Comparator.comparing((Head h) -> h.value).thenComparingInt(h -> h.stream))`。

**为什么 O(N log k)**：全局最小一定在 k 个队首里。堆里永远只放每条序列的队首（≤ k 个），每个元素进堆出堆各一次，每次 O(log k)，总计 O(N log k)，额外空间 O(k)。对比：每步线性扫描 k 个队首是 O(N·k)；有序列表挑最小 O(1) 但插入 O(k)。

演示：依次放 5,3,8,1 得 `[1,3,8,5]`，`poll` 返回 1。
