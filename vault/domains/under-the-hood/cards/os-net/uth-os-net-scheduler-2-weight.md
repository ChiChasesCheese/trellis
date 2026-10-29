---
id: uth-os-net-scheduler-2-weight
node: os-net.scheduler
type: qa
step: 2
---
## Q
**nice 值怎么变成 CPU 份额**｜Linux · 内核 7.3

nice 值只差 1，两个任务分到的 CPU 差多少？一棵树怎么同时容纳不同优先级？

## A
**结构。** 每个任务有一个权重，`vruntime` 的增长速度与权重成反比：`vruntime += 实际运行时间 × 1024 / 权重`。权重大的任务 `vruntime` 涨得慢，长期靠左，更常被选中。

**细节。**

- 权重表 `sched_prio_to_weight[40]`：nice 0 是 1024，nice 1 是 820，nice -1 是 1277，每级约 1.25 倍
- 两端：nice -20 是 88761，nice 19 是 15，相差近 6000 倍
- 两个任务 nice 差 1，份额约 55% 对 45%

**为什么。** 不给每个优先级各建一个队列，而是把优先级折进“时钟走速”，一个排序键就够了。

**对应 LeetCode：** LC 621 任务调度器 · LC 1834 单线程 CPU
