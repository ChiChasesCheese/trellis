---
id: uth-go-rust-go-channel-1-hchan
node: go-rust.go-channel
type: qa
step: 1
---
## Q
**channel 底下是什么**｜Go · 1.27 运行时

`make(chan int, 3)` 之后，数据和等待者各存在哪里？

## A
**结构。** 一个 `hchan` 结构：一把锁、一个环形缓冲区，外加接收和发送两条等待队列。

**细节。**

- 环形缓冲：`buf`、`qcount`（已有个数）、`dataqsiz`（容量）、`sendx` / `recvx`（读写下标）
- `recvq` / `sendq` 是阻塞中的 goroutine 链表
- 发送顺序：先看有没有等待的接收者，有就直接交给它；其次缓冲有空位就入队；都不行就挂到 `sendq` 睡眠

**为什么。** 所有字段由同一把互斥锁保护，实现简单；缓冲区加两个下标，入队出队都是 O(1)。

**对应 LeetCode：** LC 622 设计循环队列 · LC 1188 设计有限阻塞队列
