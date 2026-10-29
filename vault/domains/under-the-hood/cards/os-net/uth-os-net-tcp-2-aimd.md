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
**背景。** `cwnd` 该多大？太大会塞满路由器、引起丢包，太小又浪费带宽，而发送方并不知道网络的容量，只能边发边试：一开始小心，快速放大，一出事就退让。

**结构。** `cwnd` 的状态机：慢启动（slow start，从小开始成倍增长）→ 拥塞避免（congestion avoidance，接近极限后慢慢加）；丢包时乘性减（直接打折）。例：初始 10 个段（`TCP_INIT_CWND`，段 = 一次发出的数据包），慢启动每个 RTT 翻倍：10、20、40……

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<line x1="40" y1="18" x2="40" y2="170" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="40" y1="170" x2="322" y2="170" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">cwnd</text>
<text x="322" y="190" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">RTT</text>
<line x1="40" y1="70" x2="318" y2="70" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.45"/>
<text x="318" y="64" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">ssthresh</text>
<polyline points="50,156 70,150 90,136 108,112 125,70 200,40" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="200" y1="40" x2="200" y2="105" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<polyline points="200,105 275,75" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="275" y1="75" x2="275" y2="122" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<polyline points="275,122 318,104" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="60" y="120" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">慢启动</text>
<text x="130" y="108" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">拥塞避免</text>
<text x="206" y="54" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">丢包减半</text>
</svg>
```

**细节。**

- 慢启动：每个 ACK 把 `cwnd` 加上被确认的段数，每个 RTT 翻倍，直到 `ssthresh`（慢启动阈值，翻倍与线性增长的分界）
- Reno 拥塞避免：每个 RTT 加 1；丢包后 `ssthresh = max(cwnd/2, 2)`
- CUBIC（Linux 默认）丢包后只降到 717/1024 ≈ 0.7 倍，再按三次函数曲线回升

**为什么。** 先指数探测，后线性逼近，丢包猛降：探测快、逼近稳、退让快，代价是吞吐呈锯齿。

**对应 LeetCode：** 无直接对应的题
