---
id: bagu-time-wait-close-wait-2-why-2msl
node: a.net.time-wait-close-wait
type: qa
step: 2
---
## Q
**TIME_WAIT · 为什么要等 2MSL**｜必会

面试官：「主动关闭的一方为什么不能发完最后一个 ACK 就立刻关闭，非要等 2MSL？」

## A
**基本回答。** 两个原因：最后一个 ACK 可能丢了，对方收不到会重发 FIN，本端必须还在场回 ACK，否则对方一直重发到超时；让网络里属于旧连接的延迟报文自然过期，避免被相同四元组的新连接误收。2MSL 的来由：最后的 ACK 最多活 1 个 MSL（报文在网络中的最长存活时间），对方重发的 FIN 最多再活 1 个 MSL，合起来覆盖最坏情况。Linux 里 60 秒是编译期常量，不能用参数调短。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 228">
<text x="170" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">TIME_WAIT = 2×MSL（Linux 固定 60 秒）</text>
<line x1="8" y1="24" x2="332" y2="24" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="8" y="34" width="162" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="89.0" y="49.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最后的 ACK</text>
<text x="89.0" y="64.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最多存活 1 个 MSL</text>
<rect x="170" y="34" width="162" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="251.0" y="49.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重发的 FIN 最多</text>
<text x="251.0" y="64.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">再存活 1 个 MSL</text>
<text x="8" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">原因一：最后的 ACK 可能丢了</text>
<text x="8" y="118" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">对方重发 FIN，本端还在才能再回 ACK</text>
<text x="8" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">原因二：旧连接的迟到报文</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">等它们过期，别被同四元组新连接误收</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">端口还被占着：重启报 Address already in use</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">监听套接字开 SO_REUSEADDR 可立刻绑定</text>
</svg>
上方条是 2MSL 的算法，下方是等这么久的两个原因，以及端口还被占着的后果。
**业务场景。** 聊天网关发布时进程重启，新进程绑定端口失败，日志 `Address already in use`，因为旧连接还在 TIME_WAIT 占着端口；给监听套接字设 `SO_REUSEADDR` 允许在有 TIME_WAIT 时绑定，就能立刻重启。
**容易错。**
- **以为 TIME_WAIT 是浪费时间：** 它保护被动方正常关闭、新旧连接数据不串。
- **以为 tcp_fin_timeout 管 TIME_WAIT：** 它管 FIN_WAIT_2。
