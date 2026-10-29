---
id: uth-os-net-scheduler-1-rbtree
node: os-net.scheduler
type: qa
step: 1
---
## Q
**调度器怎么挑下一个任务**｜Linux · 内核 6.5 与 7.3

成千上万个可运行任务排队，Linux 怎么在 O(log n) 内挑出下一个上 CPU 的？

## A
**结构。** 红黑树（red-black tree）：可运行任务按排序键放进树里，调度器取最左节点。

**细节。**

- 6.5 的 CFS 以虚拟运行时间 `vruntime` 为键，最左 = 跑得最少、最“亏欠”的任务
- 6.6 起 EEVDF 取代 CFS，树还是红黑树，键换成虚拟截止时间 `deadline`
- 树用 `rb_root_cached` 缓存了最左节点，取下一个是 O(1)，入队出队 O(log n)

**为什么。** 一棵按“已获得服务”排序的树，替换了旧版按优先级分桶的数组队列，不再需要靠启发式猜哪个任务是交互式的。

**对应 LeetCode：** LC 729 我的日程安排表 I · LC 253 会议室 II
