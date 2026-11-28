---
id: bagu-tcp-handshake-1-three-way
node: a.net.tcp-handshake
type: qa
step: 1
---
## Q
**TCP 握手 · 为什么是三次握手，不是两次**｜必会

面试官：「TCP 建立连接为什么要三次握手？两次行不行？」

## A
**基本回答。** 三次：客户端 `SYN, seq=x`；服务端 `SYN+ACK, seq=y, ack=x+1`；客户端 `ACK, ack=y+1`。目的是双方互相确认收发能力并同步各自的初始序列号。本来是四个报文（双方各一个序列号、各需对方确认一次），中间两个合并成 SYN+ACK，所以是三次。两次不够：首要是防历史 SYN，客户端早先发的旧 SYN 滞留后才到，两次握手时服务端就建连接占资源，三次时客户端发现确认号不对会回 RST，服务端释放；另外服务端也无法确认客户端收到了自己的序列号。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<rect x="20" y="6" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端</text>
<rect x="220" y="6" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务端</text>
<line x1="70" y1="32" x2="70" y2="196" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="270" y1="32" x2="270" y2="196" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="170" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SYN，seq=x</text>
<line x1="70" y1="58" x2="270" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="270.0,84.0 262.6,86.3 263.5,79.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SYN+ACK，seq=y，ack=x+1</text>
<line x1="270" y1="106" x2="70" y2="132" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="70.0,132.0 76.5,127.9 77.4,134.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ACK，ack=y+1</text>
<line x1="70" y1="154" x2="270" y2="180" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="270.0,180.0 262.6,182.3 263.5,175.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="218" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">旧 SYN 迟到：客户端回 RST，服务端释放</text>
<text x="8" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两次握手：服务端会白白建出连接</text>
</svg>
三个箭头依次是 SYN、SYN+ACK、ACK；下方是旧 SYN 迟到的处理。
**细节。** 第三次 ACK 可以带数据，前两次一般不带；TCP Fast Open 允许在 SYN 里带数据省一个往返，但需双方支持并防重放。握手本身 1 个 RTT，HTTPS 还要再加 TLS，所以短连接频繁新建很贵，要用 keep-alive 和连接池；服务端在 SYN 到达时就建半连接对象，是 SYN 洪泛的入口。
**业务场景。** 短链接重定向多是一次性短连接，每次新建 TCP 加 TLS，用户端多出好几个往返；负载均衡到后端之间启用 keep-alive 复用连接后，后端握手开销基本消失（用户到入口那段仍每次新建）。
**容易错。**
- **以为两次握手也可靠。**
- **以为三次是凑出来的：** 本来四个报文，中间两个合并。
- **以为握手不带数据，也不花成本。**
