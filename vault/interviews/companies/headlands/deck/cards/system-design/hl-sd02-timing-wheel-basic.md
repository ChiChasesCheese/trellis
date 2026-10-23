---
id: hl-sd02-timing-wheel-basic
node: system-design.sd02-job-scheduler
type: qa
step: 15
---
## Q
时间轮（timing wheel）的数据结构是什么？插入、到期、取消各怎么做、复杂度多少？怎么保证「不早」？

## A
把时间切成 tick，用一个**环形数组**，每个槽（slot）挂一条链表，放「在这个 tick 到期的定时器」。
- 插入：slot = `(fireTick) mod wheelSize`，O(1)；
- 到期：指针扫过一个槽，整条链表一次性取出，O(到期数)；
- 取消：双向链表摘除，O(1)。

精度：任务实际在其 tick 的开始被取出，最多晚 1 tick（10 ms）。要保证**不早**，把 tick 号向上取整：`fireTick = ceil(fireAt / tickMs)`。
