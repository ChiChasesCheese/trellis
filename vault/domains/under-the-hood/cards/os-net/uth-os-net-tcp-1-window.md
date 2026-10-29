---
id: uth-os-net-tcp-1-window
node: os-net.tcp
type: qa
step: 1
---
## Q
**滑动窗口：能发多少由谁说了算**｜Linux · TCP · 内核 7.3

一条 TCP 连接任一时刻最多能有多少数据在路上没被确认？

## A
**结构。** 发送方维护一个滑动窗口：已确认 | 已发未确认 | 可发 | 暂不能发。窗口大小取 min(接收窗口 rwnd，拥塞窗口 cwnd)。

**细节。**

- 收到 ACK，窗口左边界右移，腾出新的可发空间
- 窗口字段只有 16 位（64 KB）；窗口缩放（window scale）选项最多左移 14 位（`TCP_MAX_WSCALE`），上限约 1 GB
- 发包前内核检查 `tcp_cwnd_test` 与 `tcp_snd_wnd_test`，两道关都过才发

**为什么。** rwnd 保护接收方（流量控制），cwnd 保护网络（拥塞控制），取小就是各管各的。

**对应 LeetCode：** LC 3 无重复字符的最长子串 · LC 239 滑动窗口最大值
