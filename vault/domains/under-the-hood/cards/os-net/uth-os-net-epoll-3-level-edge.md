---
id: uth-os-net-epoll-3-level-edge
node: os-net.epoll
type: qa
step: 3
---
## Q
**水平触发和边缘触发差在哪**｜Linux · epoll · 内核 7.3

一个 fd 的数据只读了一半，水平触发（LT）和边缘触发（ET）下一次 `epoll_wait` 分别怎样？

## A
**结构。** 差别就在 `ep_send_events` 把事件交给用户之后：水平触发把节点重新挂回 `rdllist`，边缘触发不挂。

**细节。**

- LT（默认）：下次 `epoll_wait` 会重新检查该 fd，还有数据就再报告
- ET（`EPOLLET`）：只有新事件到来、回调再次入链时才报告
- `EPOLLONESHOT`：报告一次就清掉事件掩码，要 `EPOLL_CTL_MOD` 重新武装

**坑。** ET 必须配非阻塞 fd，并且一次读到 `EAGAIN`，否则剩下的数据不会再有通知。

**对应 LeetCode：** LC 622 设计循环队列 · LC 707 设计链表
