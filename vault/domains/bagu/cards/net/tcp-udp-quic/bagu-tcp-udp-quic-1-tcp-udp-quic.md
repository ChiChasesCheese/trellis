---
id: bagu-tcp-udp-quic-1-tcp-udp-quic
node: b.net.tcp-udp-quic
type: qa
step: 1
---
## Q
**TCP 与 UDP · QUIC 解决了什么**｜必会

面试官：「TCP 和 UDP 有什么区别，各适合什么场景？QUIC 是什么，解决了什么问题？」

## A
**基本回答。** TCP 面向连接，可靠、有序、有拥塞控制，头部 20 字节起，适合 HTTP、数据库、文件、支付回调；UDP 无连接、不保证可靠，头部 8 字节，适合 DNS、音视频、游戏。TCP 的队头阻塞：一个包丢了，后面已到的数据也要等重传才能交给应用，HTTP/2 在一个 TCP 连接上复用多流，一个丢包卡所有流。QUIC 基于 UDP 在用户态实现可靠传输：每个流独立收发重传；握手和 TLS 1.3 合并，首次 1 个 RTT、恢复连接 0-RTT；用连接 ID 标识连接，Wi-Fi 切蜂窝连接不断（TCP 以四元组标识，要重连）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 234">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">TCP：一条字节流，按序交付</text>
<rect x="8" y="24" width="76" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46.0" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">包 1</text>
<text x="46.0" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 A</text>
<rect x="88" y="24" width="76" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="126.0" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">包 2 丢了</text>
<text x="126.0" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 B</text>
<rect x="168" y="24" width="76" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="206.0" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">包 3</text>
<text x="206.0" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 C</text>
<rect x="248" y="24" width="76" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="286.0" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">包 4</text>
<text x="286.0" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 A</text>
<text x="10" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">包 3、4 已到，也得等包 2 重传</text>
<line x1="10" y1="90" x2="330" y2="90" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="10" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">QUIC：每个流独立收发和重传</text>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">流 A</text>
<rect x="54" y="120" width="80" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="94.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">包 1</text>
<rect x="144" y="120" width="80" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="184.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">包 4</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">流 B</text>
<rect x="54" y="154" width="170" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="139.0" y="171.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">包 2 丢了，重传</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">流 C</text>
<rect x="54" y="188" width="80" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="94.0" y="205.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">包 3</text>
<text x="10" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有流 B 等，流 A、C 照常交付</text>
</svg>
TCP 里包 2 丢了，已到的包 3、4 也要等；QUIC 里只有流 B 等重传，流 A、C 照常交付。
**为什么基于 UDP。** TCP 在内核里，改协议要升级全网内核和中间设备；新的传输层协议号会被中间设备丢弃。UDP 能穿透 NAT 和防火墙，用户态实现可快速迭代。代价：CPU 开销更大，部分网络限制 UDP，中间设备无法优化。TCP 和 UDP 端口空间相互独立，同一端口号可各绑一次。
**业务场景。** 直播推流和实时互动更看重延迟，倾向 UDP 或 QUIC；支付回调要求可靠，走 TCP。
**容易错。**
- **以为 UDP 一定比 TCP 快：** 只是少了握手、重传和拥塞控制，自己实现可靠性也有开销。
- **以为 HTTP/2 解决了队头阻塞：** 只解决应用层。
