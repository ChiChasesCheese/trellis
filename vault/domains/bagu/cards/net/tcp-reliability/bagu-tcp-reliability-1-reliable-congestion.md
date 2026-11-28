---
id: bagu-tcp-reliability-1-reliable-congestion
node: b.net.tcp-reliability
type: qa
step: 1
---
## Q
**TCP 可靠传输 · 重传、滑动窗口与拥塞控制**｜必会

面试官：「TCP 是怎么保证可靠传输的？流量控制和拥塞控制有什么区别？为什么跨洋链路上传文件会慢？」

## A
**基本回答。** 可靠靠序列号加 ACK、超时重传（RTO 按测得的 RTT 动态算）、校验和、乱序重组和去重；收到 3 个重复 ACK 就快速重传，不等超时。流量控制保护接收方：ACK 里通告 rwnd，窗口随 ACK 滑动所以能连续发，窗口为 0 时定期探测。拥塞控制保护网络：发送量取 `min(cwnd, rwnd)`；慢启动 cwnd 每个 RTT 翻倍，到 ssthresh 后拥塞避免每个 RTT 加一个 MSS；3 个重复 ACK 则折半进快速恢复，超时才回到 1。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 292">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">cwnd</text>
<line x1="30" y1="20" x2="30" y2="172" stroke-width="1.2" stroke="currentColor"/>
<line x1="30" y1="172" x2="332" y2="172" stroke-width="1.2" stroke="currentColor"/>
<text x="332" y="188" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时间（RTT）</text>
<line x1="30" y1="110" x2="125" y2="110" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="36" y="104" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ssthresh</text>
<line x1="35" y1="164" x2="65" y2="156" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="65" y1="156" x2="95" y2="140" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="95" y1="140" x2="125" y2="110" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="125" y1="110" x2="215" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="215" y1="80" x2="215" y2="125" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="215" y1="125" x2="270" y2="105" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="270" y1="105" x2="270" y2="164" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="270" y1="164" x2="290" y2="158" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="290" y1="158" x2="310" y2="146" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="310" y1="146" x2="330" y2="125" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="72" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="165" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="224" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<text x="278" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<text x="10" y="210" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 慢启动：每个 RTT 翻倍，到 ssthresh</text>
<text x="10" y="228" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">2 拥塞避免：每个 RTT 加一个 MSS</text>
<text x="10" y="246" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3 三个重复 ACK：cwnd 折半，快速恢复</text>
<text x="10" y="264" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">4 超时：cwnd 回到 1，重新慢启动</text>
<text x="10" y="284" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">发送量 = min(cwnd, rwnd)</text>
</svg>
横轴 RTT，纵轴 cwnd：先指数爬升，过阈值线性增长，3 个重复 ACK 折半，超时掉回 1。
**跨洋为什么慢。** 主要是 RTT 大，慢启动每翻一轮就要等一个 RTT，初始窗口 `initcwnd` 默认 10 个 MSS（约 14KB）。传 1MB（约 720 个 MSS，MSS 约 1460 字节）只算慢启动：10、20、40、80、160、320 前 6 轮共 630 个，第 7 轮发完，共 7 个 RTT；RTT 5ms 约 35ms，RTT 150ms 约 1 秒多。Linux 默认 CUBIC（基于丢包，实测内核默认值）；BBR 基于带宽和 RTT 估计，在高延迟有随机丢包的跨洋链路吞吐更好。降首包延迟：就近接入（CDN、边缘）、复用连接、TLS 1.3 与会话恢复、QUIC 0-RTT。
**业务场景。** 跨境链路丢包率 1%，每次丢包 cwnd 折半，单连接吞吐大幅下降，回传大账单文件很慢；分块多连接并行各自爬窗口，加就近接入点。
**容易错。**
- **混淆流量控制和拥塞控制：** 前者 rwnd 保护接收方，后者 cwnd 保护网络。
- **以为丢包都从 1 开始：** 只有超时才回 1。
- **以为 BBR 是 Linux 默认：** 默认 CUBIC。
