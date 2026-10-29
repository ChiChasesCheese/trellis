---
id: uth-redis-event-loop-persistence-1-event-loop
node: redis.event-loop-persistence
type: qa
step: 1
---
## Q
**单线程的 Redis 为什么够快**｜Redis · 8.10

执行命令基本只用一个线程，Redis 为什么还能扛住很高的吞吐？

## A
**结构。** 事件循环（event loop）：一个线程反复“等 I/O 就绪 → 处理命令 → 跑定时任务”，等 I/O 靠操作系统的多路复用。

**细节。**

- 按平台选：Linux 用 `epoll`，macOS / BSD 用 `kqueue`，兜底是 `select`
- 数据在内存里；单线程执行，数据结构不用加锁
- `io-threads` 默认是 1；调大后，套接字读写和协议解析交给 I/O 线程

**为什么。** 单线程免去锁和上下文切换；想用多核就多开几个实例。

**坑。** 一个慢命令（如 `KEYS *`）会让所有客户端排队。

**对应 LeetCode：** LC 933 最近的请求次数 · LC 622 设计循环队列
