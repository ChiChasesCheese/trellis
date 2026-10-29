%% trellis:begin %%
# 可删除、可改优先级的堆：堆 + 下标
*数据结构组合：开源框架里的类设计*

定时任务要能取消、优先级要能改：普通堆删中间元素要 O(n) 找位置；每个元素记住自己在堆数组里的下标（Java DelayedWorkQueue 的 heapIndex、Go container/heap 文档里的 index 字段），删和改都是 O(log n)。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-compose-indexed-heap-1-needs]]
2. [[uth-compose-indexed-heap-2-structures]]
3. [[uth-compose-indexed-heap-3-invariants-code]]
4. [[uth-compose-indexed-heap-4-real]]
5. [[uth-compose-indexed-heap-5-removable-scheduler]]
%% trellis:end %%

## Notes
