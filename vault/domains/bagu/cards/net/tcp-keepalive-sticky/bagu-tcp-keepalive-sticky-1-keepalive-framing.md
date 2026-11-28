---
id: bagu-tcp-keepalive-sticky-1-keepalive-framing
node: b.net.tcp-keepalive-sticky
type: qa
step: 1
---
## Q
**TCP Keepalive · 心跳、粘包与连接异常**｜追问

面试官：「长连接网关怎么发现对端已死？TCP Keepalive 和 HTTP Keep-Alive 是一回事吗？拔网线、进程崩溃时连接分别什么表现？粘包怎么解决？」

## A
**基本回答。** TCP Keepalive（内核在空闲连接上发探测包问对端死活，默认关闭）和 HTTP Keep-Alive（复用同一条 TCP 连接发多个请求）不是一回事。内核默认开启后空闲 7200 秒才探测，间隔 75 秒、连探 9 次，约 7875 秒（两小时多）才判死，所以长连接网关用应用层心跳：间隔和超时自己定（如 30 秒一次、连续 3 次无 pong 约 90 秒断开），还能发现应用卡死（内核探测只证明对端内核活着）并维护在线状态。粘包是因为 TCP 是字节流没有消息边界，办法：定长、分隔符（内容含分隔符要转义）、包头带长度字段（最常用，先读 4 字节得 N 再读 N 字节）；UDP 面向报文没这个问题。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<rect x="6" y="6" width="150" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">进程崩溃</text>
<line x1="156" y1="26" x2="165.0" y2="26.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="172,26 165.0,29.2 165.0,22.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178" y="23" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">内核回收资源时发 FIN，</text>
<text x="178" y="39" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">对端立刻知道</text>
<rect x="6" y="53" width="150" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拔网线，有数据</text>
<line x1="156" y1="73" x2="165.0" y2="73.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="172,73 165.0,76.2 165.0,69.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178" y="70" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">重传 tcp_retries2=15 次，</text>
<text x="178" y="86" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">约 15 分钟后内核断开</text>
<rect x="6" y="100" width="150" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拔网线，没数据，</text>
<text x="81" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没开 Keepalive</text>
<line x1="156" y1="120" x2="165.0" y2="120.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="172,120 165.0,123.2 165.0,116.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178" y="117" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">连接一直 ESTABLISHED，</text>
<text x="178" y="133" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">双方都不知道</text>
<rect x="6" y="147" width="150" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="163.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TCP Keepalive</text>
<text x="81" y="178.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（内核默认值）</text>
<line x1="156" y1="167" x2="165.0" y2="167.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="172,167 165.0,170.2 165.0,163.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178" y="164" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">空闲 7200 秒才开始探测，</text>
<text x="178" y="180" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">间隔 75 秒、连探 9 次</text>
<rect x="6" y="194" width="150" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="81" y="210.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用层心跳</text>
<text x="81" y="225.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30 秒一次</text>
<line x1="156" y1="214" x2="165.0" y2="214.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="172,214 165.0,217.2 165.0,210.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178" y="211" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">连续 3 次没回就断开，</text>
<text x="178" y="227" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">约 90 秒发现</text>
</svg>
进程崩溃，内核回收时发 FIN，对端立刻知道；拔网线有数据在发，按 `tcp_retries2`（默认 15）重传约 15 分钟后断开，中途插回网线还能恢复；拔网线又没数据、没开 Keepalive，两端都一直显示 ESTABLISHED。主机掉电内核来不及发包，只能靠 Keepalive 或心跳发现。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发送方连写三条消息（字母 = 字节）</text>
<rect x="10" y="22" width="30" height="26" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="25" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="40" y="22" width="30" height="26" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="55" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="70" y="22" width="30" height="26" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="100" y="22" width="30" height="26" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="130" y="22" width="30" height="26" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="160" y="22" width="30" height="26" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="175" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<rect x="190" y="22" width="30" height="26" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="205" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<rect x="220" y="22" width="30" height="26" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="235" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<rect x="250" y="22" width="30" height="26" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="265" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<line x1="145" y1="50" x2="145.0" y2="69.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="145,76 141.8,69.0 148.2,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="153" y="68" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">TCP 当成一条字节流</text>
<rect x="10" y="80" width="30" height="26" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="25" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="40" y="80" width="30" height="26" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="55" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="70" y="80" width="30" height="26" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="100" y="80" width="30" height="26" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="130" y="80" width="30" height="26" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="160" y="80" width="30" height="26" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="175" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<rect x="190" y="80" width="30" height="26" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<rect x="220" y="80" width="30" height="26" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<rect x="250" y="80" width="30" height="26" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="265" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<line x1="130" y1="74" x2="130" y2="116" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<line x1="10" y1="118" x2="127" y2="118" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="10" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 1 次 read：AAAB</text>
<line x1="133" y1="118" x2="280" y2="118" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="133" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 2 次 read：BCCCC</text>
<text x="10" y="162" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">B 被拦腰切成两半：要靠包头里的长度字段切回消息</text>
</svg>
三条消息在字节流里连在一起，一次 `read` 可能读到半条，接收方必须自己找到消息边界。
**业务场景。** 直播长连接网关，用户手机进电梯断网没发 FIN，服务端连接仍是 ESTABLISHED；只靠默认 Keepalive 要约 2 小时 11 分才发现，期间一直占内存。应用层心跳 30 秒一次，连续 3 次没回后主动关闭、释放内存并标为离线。
**容易错。**
- **把 HTTP Keep-Alive 当心跳：** 它不探测对端死活。
- **以为拔网线连接立刻断。**
- **以为一次 send 对应一次 recv。**
