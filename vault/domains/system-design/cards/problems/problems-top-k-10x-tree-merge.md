---
id: problems-top-k-10x-tree-merge
node: problems.search.top-k
type: qa
step: 8
tags: [grown]
---
## Q
In a Top-K trending design, when event volume grows 10x, why does the Count-Min Sketch / Space-Saving memory footprint stay manageable, and what becomes the new bottleneck instead?

## A
Both structures' memory scales as O(1/ε), independent of the number of distinct items — holding the same absolute error target after a 10x volume increase just requires shrinking ε roughly 10x (e.g. Count-Min Sketch width grows about 10x, moving memory from tens of MB to roughly ten times that), which stays a manageable, linear cost. The bottleneck that actually emerges is the merge step's fan-in: the number of shards or sub-shards whose sketches must be summed cell-by-cell grows with volume, so a flat fan-in into one coordinator node becomes the new limiting point. The fix is the same idea used for rolling up time windows, applied to topology instead: merge sketches in a tree (sub-shards merge pairwise within a rack or availability zone first, then those partial merges combine at the next level up) rather than flat fan-in to a single node.

## Q zh
在一个热门榜设计中，当事件量增长 10 倍时，为什么 Count-Min Sketch / Space-Saving 的内存占用依然可控？新的瓶颈会出现在哪里？

## A zh
两种结构的内存都是 `O(1/ε)`，与不同 item 的个数无关——事件量增长 10 倍后要维持同样的绝对误差目标，只需要把 ε 缩小大约 10 倍（例如 Count-Min Sketch 的宽度增长约 10 倍，内存从几十 MB 变成大约十倍），仍然是可控的线性代价。真正冒出来的瓶颈是合并这一步的扇入：需要按 cell 相加的分片/子分片数量会随流量线性增长，扁平地扇入一个协调节点会成为新的限制点。修复思路和时间窗口的滚动汇总是同一个道理，只是换成了拓扑维度：把 sketch 的合并做成树形（子分片先在机架或可用区内部两两合并，再往上一级合并），而不是扁平地全部扇入一个节点。
