---
id: bagu-nagle-delayed-ack-1-forty-ms
node: b.net.nagle-delayed-ack
type: qa
step: 1
---
## Q
**Nagle 算法与延迟确认 · 固定多出 40ms**｜追问

面试官：「小包 RPC 偶尔固定多出约 40ms 延迟，排查下来是 Nagle 和延迟确认叠加。原理是什么，怎么解决？」

## A
**基本回答。** Nagle：有未确认的小包在途时，后续小数据先攒着，凑满一个 MSS 或收到 ACK 才发，目的是省小包的头部开销。延迟确认（delayed ACK）：接收方等一小会儿（Linux 最多约 40ms），想把 ACK 捎带在回复里或凑两个包一起确认。触发模式是写—写—读：先发小包 A，B 要等 A 的 ACK，而对端读不完请求不会回复、没数据可捎带，只能等到超时，多出约 40ms；一次写完整请求不会触发。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="70" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">客户端</text>
<text x="270" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">服务端</text>
<line x1="70" y1="22" x2="70" y2="206" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="270" y1="22" x2="270" y2="206" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="70" y1="38" x2="270" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="270.0,52.0 263.4,54.4 263.8,48.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">小包 A</text>
<text x="170" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">B 要等 A 的 ACK（Nagle）</text>
<text x="170" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对端想捎带回复，先不回 ACK</text>
<rect x="105" y="104" width="130" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="121.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">约 40ms 白等</text>
<line x1="270" y1="152" x2="70" y2="166" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,166.0 76.2,162.7 76.6,168.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ACK（超时才发）</text>
<line x1="70" y1="186" x2="270" y2="200" stroke-width="1.2" stroke="currentColor"/>
<polygon points="270.0,200.0 263.4,202.4 263.8,196.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">小包 B</text>
<text x="10" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">TCP_NODELAY：A、B 立刻发，不等 ACK</text>
</svg>
B 等 A 的 ACK，服务端等着捎带回复，约 40ms 超时才单独发 ACK，之后 B 才发出；`TCP_NODELAY` 则 A、B 立刻发。
**解决与代价。** 实测（Linux 容器内回环，先后 `send` 两个小包再读回复）默认每次约 41~45ms，设 `TCP_NODELAY` 后接近 0；新连接第一轮立即确认，所以第一轮是 0。优先在应用层把头和体合并成一次 `write`，再对低延迟场景设 `TCP_NODELAY`（多数 RPC 框架默认已开）。关掉 Nagle 后小消息频繁时包数增多、头部开销大；要攒包用 `TCP_CORK`。
**业务场景。** 支付网关给下游发请求，头和体分两次 `write`：头立即发出成为包 A，体被 Nagle 攒着等 ACK，下游读不完请求不回复，约 40ms 后才单独回 ACK，接口耗时稳定多 40ms，抓包能看到第二个包在等 ACK；合并成一次写后消失。
**容易错。**
- **以为是网络慢：** 固定约 40ms 是两个机制叠加。
- **以为 TCP_NODELAY 总是好的：** 小消息频繁时增加包处理压力。
