---
id: uth-os-net-tcp-3-bbr
node: os-net.tcp
type: qa
step: 3
---
## Q
**BBR 不看丢包，看什么**｜Linux · tcp_bbr · 内核 7.3

CUBIC 靠丢包判断拥塞，BBR 靠什么调速度？

## A
**结构。** BBR 持续估计两个量：瓶颈带宽 = 最近 10 个往返里的最大交付速率（windowed max），最小 RTT = 最近 10 秒里的最小值（windowed min）。

**细节。**

- 发送速率 = `pacing_gain` × 瓶颈带宽；`cwnd` = 2 × 带宽 × `min_rtt`
- 稳态循环：增益 5/4（探测更多带宽）→ 3/4（排空队列）→ 1.0 巡航
- 启动阶段增益取 2/ln2 ≈ 2.89，是让发送速率每个 RTT 翻倍的最小增益

**为什么。** 丢包不等于拥塞，而队列堆积会让延迟暴涨；直接建模“管道容量 = 带宽 × RTT”更稳。

**对应 LeetCode：** LC 239 滑动窗口最大值 · LC 1011 在 D 天内送达包裹的能力
