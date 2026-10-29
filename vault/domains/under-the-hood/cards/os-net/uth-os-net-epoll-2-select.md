---
id: uth-os-net-epoll-2-select
node: os-net.epoll
type: qa
step: 2
---
## Q
**select 为什么撑不住大量连接**｜Linux · select 对比 epoll

`select` 每次调用都要做什么？为什么 fd 一多就线性变慢，还有 1024 的上限？

## A
**结构。** `fd_set` 是定长位图，`FD_SETSIZE` 是 1024 位。

**细节。**

- 每次调用，内核先把位图拷进来，再在 `do_select` 里对每个关心的 fd 调一次 `poll`，O(n)
- 返回时结果位图拷回用户态，用户还得再扫一遍找出就绪的 fd
- epoll 登记一次后，`epoll_wait` 只拿就绪事件

**为什么。** 位图本身很简单，但“每次都把全部关心的 fd 交给内核”的接口，决定了 O(n)，与实现多快无关。

**对应 LeetCode：** LC 191 位1的个数 · LC 338 比特位计数
