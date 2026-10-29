---
id: uth-go-rust-go-scheduler-2-steal
node: go-rust.go-scheduler
type: qa
step: 2
---
## Q
**空闲的 P 怎么找活干**｜Go · 1.27 运行时

某个 P 的本地队列空了，它怎么拿到别人的 goroutine？

## A
**结构。** 工作窃取（work stealing）：空闲 P 随机挑别的 P，从它的本地队列里偷走一半。

**细节。**

- 每次偷 `n - n/2` 个，也就是队列长度的一半向上取整
- 找活最多重试 4 轮，最后一轮才会去偷对方的 `runnext`
- 每调度 61 次（`schedtick % 61`）先看一眼全局队列

**为什么。** 偷一半让负载一次就平摊开；每 61 次查全局队列，避免两个互相唤醒的 goroutine 一直占着本地队列，全局队列里的 goroutine 饿死。

**对应 LeetCode：** LC 1834 单线程 CPU · LC 621 任务调度器
