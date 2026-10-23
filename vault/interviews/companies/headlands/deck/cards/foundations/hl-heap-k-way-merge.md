---
id: hl-heap-k-way-merge
node: foundations.heap-priority-queue
type: qa
step: 20
---
## Q
用堆做 K 路归并怎么做？复杂度是多少，比另外两种笨办法好在哪？

## A
K 条已排序的流，堆里放 K 个元素（每条流当前的队头，如（值，流编号，下标））。反复：`poll` 出最小的 → 输出 → 把这条流的下一个元素 `offer` 进去。每输出一个 O(log K)，总共 **O(N log K)**，空间 O(K)。比较器加流编号做平局裁决保证稳定。

对比：全部拼起来再排序 O(N log N)；依次两两合并 O(N·K)。堆版本两者都更好，而且是**流式**的，不必一次读完所有数据。
