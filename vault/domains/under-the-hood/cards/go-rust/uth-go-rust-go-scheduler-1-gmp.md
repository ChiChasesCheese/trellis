---
id: uth-go-rust-go-scheduler-1-gmp
node: go-rust.go-scheduler
type: qa
step: 1
---
## Q
**goroutine 排在哪里等 CPU**｜Go · 1.27 运行时

Go 调度器里的 G、M、P 各是什么？可运行的 goroutine 存在哪种队列里？

## A
**结构。** G 是 goroutine，M 是系统线程，P 是调度上下文（数量即 `GOMAXPROCS`，默认逻辑核数）；每个 P 自带一个本地运行队列。

**细节。**

- 本地队列是长度 256 的环形数组（`runq [256]guintptr`），靠原子操作而非锁访问
- 另有 `runnext` 槽：刚被当前 G 唤醒的 G 优先运行，适合来回通信的一对 goroutine
- 本地队列放满时，把一半（128 个）连同新来的搬到全局队列

**为什么。** 每个 P 各管各的队列，调度时几乎不抢锁；全局队列只当溢出区。

**对应 LeetCode：** LC 622 设计循环队列 · LC 641 设计循环双端队列
