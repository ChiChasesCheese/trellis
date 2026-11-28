---
id: bagu-tcp-handshake-4-four-way
node: a.net.tcp-handshake
type: qa
step: 4
---
## Q
**TCP 挥手 · 为什么挥手需要四次，什么情况下变成三次**｜必会

面试官：「TCP 断开连接为什么是四次挥手？有没有可能变成三次？」

## A
**基本回答。** TCP 全双工，每个方向单独关闭：主动方 `FIN`；被动方回 `ACK`（它可能还有数据要发，这段叫半关闭，收到 FIN 只表示对方不再发送）；被动方发完、应用 `close()` 后发自己的 `FIN`；主动方回 `ACK` 进入 TIME_WAIT，被动方进入 CLOSE_WAIT。ACK 和 FIN 的时机由应用 `close()` 决定，内核只能先回 ACK，所以通常四次；被动方收到 FIN 时已无数据要发、又开了延迟确认，内核可把 ACK 和 FIN 合并成一个报文，就是三次，逻辑上仍是四个动作。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 284">
<rect x="20" y="6" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主动方</text>
<rect x="220" y="6" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">被动方</text>
<line x1="70" y1="32" x2="70" y2="236" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="270" y1="32" x2="270" y2="236" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="170" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① FIN</text>
<line x1="70" y1="58" x2="270" y2="82" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="270.0,82.0 262.7,84.3 263.4,78.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② ACK</text>
<line x1="270" y1="104" x2="70" y2="128" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,128.0 76.6,124.0 77.3,130.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">被动方可能还有数据要发</text>
<text x="170" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（半关闭）</text>
<text x="170" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ FIN</text>
<line x1="270" y1="198" x2="70" y2="222" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="70.0,222.0 76.6,218.0 77.3,224.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="238" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ ACK</text>
<line x1="70" y1="244" x2="270" y2="268" stroke-width="1.2" stroke="currentColor"/>
<polygon points="270.0,268.0 262.7,270.3 263.4,264.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>
① FIN ② ACK 之间被动方还能继续发数据（半关闭）；③ FIN ④ ACK 后才彻底结束。
**细节。** 优雅关闭用 `shutdown(SHUT_WR)` 只关写方向；直接 `close()` 时若接收缓冲区有未读数据，会发 RST 而不是 FIN，对端看到连接被重置。
**业务场景。** 聊天网关发布重启：先停接新连接，通知客户端稍后重连，再分批关旧连接走完四次挥手；直接杀进程会让所有连接收到 RST，客户端同时重连，形成重连风暴。
**容易错。**
- **以为收到 FIN 就整条连接断了。**
- **以为 close() 一定发 FIN。**
