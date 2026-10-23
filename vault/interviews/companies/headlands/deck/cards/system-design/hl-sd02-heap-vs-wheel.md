---
id: hl-sd02-heap-vs-wheel
node: system-design.sd02-job-scheduler
type: qa
step: 14
---
## Q
管理定时器时，优先队列（堆）与时间轮（timing wheel）的复杂度和实际差别是什么？什么时候选哪个？

## A
- **堆**：插入 / 删除 O(log n)，取最小 O(1)；10⁶ 级定时器每个操作约 20 次比较、随机访存；JDK 的 `DelayQueue` / `ScheduledThreadPoolExecutor` 每个定时器一个对象，GC 压力大；取消是随机删除 O(n) 或惰性删除（留墓碑）；优点是任意精度、实现简单、n 小时更快；
- **时间轮**（Varghese & Lauck, 1987）：插入 / 取消 **O(1)**，到期扫描 O(到期数)，分层后每个定时器最多降级（层数 − 1）次，均摊 O(1)；可用并行数组零分配；双向链表 O(1) 摘除；精度最多晚 1 tick。

选择：n 在 10⁵ 以下用堆；10⁶ 以上、取消频繁、对象要零分配，用分层时间轮。
