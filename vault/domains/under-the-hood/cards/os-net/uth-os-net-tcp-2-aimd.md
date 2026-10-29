---
id: uth-os-net-tcp-2-aimd
node: os-net.tcp
type: qa
step: 2
---
## Q
**慢启动与加性增乘性减**｜Linux · TCP Reno 与 CUBIC · 内核 7.3

新连接一开始发多少？丢包之后窗口怎么调？

## A
**结构。** 拥塞窗口 `cwnd` 的状态机：慢启动（slow start）→ 拥塞避免（congestion avoidance）；丢包时乘性减。

**细节。**

- 初始 `cwnd` 是 10 个段（`TCP_INIT_CWND`）
- 慢启动：每个 ACK 把 `cwnd` 加上被确认的段数，每个 RTT 翻倍，直到 `ssthresh`
- Reno 拥塞避免：每个 RTT 加 1；丢包后 `ssthresh = max(cwnd/2, 2)`
- CUBIC（Linux 默认）丢包后只降到 717/1024 ≈ 0.7 倍，再按三次函数回升

**为什么。** 先指数探测，后线性逼近，丢包猛降：探测快、逼近稳、退让快，代价是吞吐呈锯齿。

**对应 LeetCode：** LC 278 第一个错误的版本 · LC 875 爱吃香蕉的珂珂
