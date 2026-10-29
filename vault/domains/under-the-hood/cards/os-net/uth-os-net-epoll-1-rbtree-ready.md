---
id: uth-os-net-epoll-1-rbtree-ready
node: os-net.epoll
type: qa
step: 1
---
## Q
**epoll 为什么不用扫描所有 fd**｜Linux · epoll · 内核 7.3

一个 epoll 监听 10 万个连接，`epoll_wait` 为什么仍然很快？

## A
**结构。** 每个 epoll 实例（`struct eventpoll`）有两个核心结构：红黑树 `rbr` 存所有被监听的 fd，就绪链表 `rdllist` 只存已就绪的。

**细节。**

- `epoll_ctl(ADD)` 把 fd 插进红黑树（O(log n)），并在该 fd 的等待队列上挂回调 `ep_poll_callback`
- 数据到达时，回调把对应节点 `list_add_tail` 进 `rdllist`
- `epoll_wait` 只遍历 `rdllist`，开销是 O(就绪数)，与监听总数无关

**为什么。** 把“登记”和“等待”拆开：登记一次，之后由事件推动，而不是每次调用都把所有 fd 重新问一遍。

**对应 LeetCode：** LC 220 存在重复元素 III · LC 707 设计链表
