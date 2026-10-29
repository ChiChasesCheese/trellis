---
id: uth-go-rust-go-channel-2-unbuffered
node: go-rust.go-channel
type: qa
step: 2
---
## Q
**无缓冲 channel 的数据停在哪**｜Go · 1.27 运行时

`make(chan int)` 没有缓冲区，发送的值经过谁的手到达接收者？

## A
**结构。** 不经过任何缓冲：值在两个 goroutine 的栈之间直接拷贝一次（`sendDirect` / `recvDirect`），再唤醒睡着的一方。

**细节。**

- 谁先到谁排进等待队列：接收者先到就睡在 `recvq` 等值，发送者先到就睡在 `sendq`
- 有缓冲且已满时，接收者取走队首，同时让阻塞的发送者把值放到刚空出的那一格

**为什么。** 不用分配缓冲，也让“发送返回”等于“对方已收到”。

**对应 LeetCode：** LC 1114 按序打印 · LC 1115 交替打印 FooBar
