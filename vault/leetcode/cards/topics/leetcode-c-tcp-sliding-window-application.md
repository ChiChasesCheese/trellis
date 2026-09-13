---
id: leetcode-c-tcp-sliding-window-application
node: topics.uncategorised
type: qa
anki: 1787361363822
tags: [algorithm::cumulative-ack, algorithm::sequence-number, algorithm::sliding-window, application, case, case::tcp-sliding-window, category::distributed-streaming, chapter::01, leetcode, system::tcp]
---
## Q
TCP 的 sliding window 如何对应双指针？为什么 advertised window 不是拥塞控制？

## A
累计 ACK 推进已确认前缀，也就是左边界；接收端通告窗口决定 flow-control 右边界。发送端实际还能发送多少，还要再受 congestion window 限制，两者解决的问题不同。

**Evidence**

RFC 9293 定义了 SND.UNA、SND.NXT、RCV.NXT 与 advertised receive window 的序号空间不变量。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdistributed-streaming%2FTCP%20%E6%B5%81%E9%87%8F%E6%8E%A7%E5%88%B6%EF%BC%9A%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3%E4%B8%8E%E7%B4%AF%E8%AE%A1%E7%A1%AE%E8%AE%A4)
