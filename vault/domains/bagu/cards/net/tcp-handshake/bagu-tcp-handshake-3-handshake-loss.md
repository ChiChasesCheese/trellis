---
id: bagu-tcp-handshake-3-handshake-loss
node: a.net.tcp-handshake
type: qa
step: 3
---
## Q
**TCP 握手 · 第一、二、三次握手丢失会发生什么**｜必会

面试官：「三次握手的三个报文，分别丢了会怎样？客户端连接超时一般是哪一步出的问题？」

## A
**基本回答。** ① SYN 丢：客户端超时重传 SYN，初始 1 秒、每次翻倍（0、1、3、7 秒），次数由 `tcp_syn_retries` 控制（当前内核默认 6），约两分钟后放弃，应用报连接超时。② SYN+ACK 丢：客户端继续重传 SYN，服务端也重传 SYN+ACK（`tcp_synack_retries`，默认 5）。③ ACK 丢：TCP 只重传带数据或 SYN、FIN 的报文，纯 ACK 不重传，服务端仍在半连接状态，重传 SYN+ACK；客户端已认为连上，先发的数据带 ACK，到达后服务端连接就建立。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<rect x="8" y="6" width="110" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="63.0" y="28.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① SYN 丢</text>
<rect x="126" y="6" width="206" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="229.0" y="28.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端超时重传 SYN</text>
<rect x="8" y="50" width="110" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63.0" y="72.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② SYN+ACK 丢</text>
<rect x="126" y="50" width="206" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="229.0" y="64.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端重传 SYN，</text>
<text x="229.0" y="79.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务端重传 SYN+ACK</text>
<rect x="8" y="94" width="110" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63.0" y="116.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ ACK 丢</text>
<rect x="126" y="94" width="206" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="229.0" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">纯 ACK 不重传，</text>
<text x="229.0" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务端重传 SYN+ACK</text>
<text x="8" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SYN 重传间隔：初始 1 秒，每次翻倍</text>
<line x1="14" y1="186" x2="326" y2="186" stroke-width="1.2" stroke="currentColor"/>
<line x1="20" y1="178" x2="20" y2="194" stroke-width="1.2" stroke="currentColor"/>
<text x="20" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SYN</text>
<text x="20" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0 秒</text>
<line x1="80" y1="178" x2="80" y2="194" stroke-width="1.2" stroke="currentColor"/>
<text x="80" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SYN</text>
<text x="80" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 秒</text>
<line x1="140" y1="178" x2="140" y2="194" stroke-width="1.2" stroke="currentColor"/>
<text x="140" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SYN</text>
<text x="140" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 秒</text>
<line x1="200" y1="178" x2="200" y2="194" stroke-width="1.2" stroke="currentColor"/>
<text x="200" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SYN</text>
<text x="200" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7 秒</text>
<line x1="260" y1="178" x2="260" y2="194" stroke-width="1.2" stroke="currentColor"/>
<text x="260" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">……</text>
<text x="8" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">tcp_syn_retries 默认 6，约两分钟后放弃</text>
<text x="8" y="258" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">tcp_synack_retries 默认 5</text>
</svg>
上半是三个报文各自丢了的后果；下半是 SYN 重传的节奏。
**排查。** 抓包看握手停在哪一步：只有 SYN 重传没有 SYN+ACK，查网络路径、防火墙、安全组和服务端监听队列（`ss -lnt` 看 Recv-Q 与 Send-Q，`netstat -s` 看溢出）；有 SYN+ACK 但没后续，查客户端侧 NAT。全连接队列满时（`tcp_abort_on_overflow=0`）直接丢第三次 ACK，客户端看起来连上了却收不到响应。连接超时反映握手问题，1 到 3 秒就够，要与读超时分开设。
**业务场景。** 支付网关调渠道偶发连接超时，抓包只见客户端 SYN 在 1、3、7 秒重传、没有 SYN+ACK，卡在第一次握手；查到对端监听队列满、SYN 被丢弃。缩短连接超时让失败快速暴露并换实例重试。
**容易错。**
- **以为丢了的 ACK 会被重传。**
- **连接超时和读超时共用一个值：** 握手问题会被拖成很慢的失败。
- **客户端显示连上了就一定正常：** 全连接队列满时收不到响应。
