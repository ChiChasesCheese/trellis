---
id: uth-os-net-scheduler-3-eevdf
node: os-net.scheduler
type: qa
step: 3
---
## Q
**EEVDF：先合格再比截止时间**｜Linux · 内核 6.6 起

6.6 起的 EEVDF 比 CFS 多了什么？想要低延迟的任务怎么优先上 CPU？

## A
**结构。** 仍是红黑树，按虚拟截止时间排序：`deadline = vruntime + slice / 权重`。每个节点还记着子树里最小的 `min_vruntime`（增强红黑树）。

**细节。**

- 先要“合格”（eligible，即还被欠着 CPU），再从合格者里选截止时间最早的
- 靠 `min_vruntime` 剪掉没有合格节点的子树，挑选仍是 O(log n)
- 默认请求时长 `sysctl_sched_base_slice` 是 0.7 ms（再按 CPU 数缩放），任务可以用 `sched_setattr()` 要更短的

**为什么。** 短 slice 的截止时间更早，延迟敏感的任务无需靠加权重（那会多占 CPU）就能更快被选中。

**对应 LeetCode：** LC 307 区域和检索 - 数组可修改 · LC 732 我的日程安排表 III
