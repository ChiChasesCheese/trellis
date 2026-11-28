---
id: bagu-tcp-handshake-5-syn-flood
node: a.net.tcp-handshake
type: qa
step: 5
---
## Q
**TCP 握手 · SYN 攻击是什么，半连接队列满了怎么办**｜追问

面试官：「线上有人发大量伪造的 SYN，正常用户连不上了。这是什么攻击？你怎么应对？」

## A
**基本回答。** SYN 洪泛：攻击者伪造大量源 IP 发 SYN，服务端为每个建半连接（SYN-RECV）并回 SYN+ACK，永远等不到第三次 ACK，半连接队列占满，正常用户的 SYN 被丢弃。按 IP 封禁没用，源地址是伪造的。对策：开 SYN cookies（`net.ipv4.tcp_syncookies=1`，队列满时不存状态，把信息编进 SYN+ACK 的序列号，收到合法第三次 ACK 再从确认号还原并建连接，耗不掉内存）；调大队列要同时调 `tcp_max_syn_backlog`、`net.core.somaxconn` 和 `listen()` 的 backlog，三者取小；攻击时调小 `tcp_synack_retries`（默认 5）让半连接更快清掉；入口层清洗。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<text x="6" y="60" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">SYN</text>
<line x1="28" y1="56" x2="40" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="40.0,56.0 33.0,59.2 33.0,52.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="40" y="34" width="84" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82.0" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">半连接队列</text>
<text x="82.0" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SYN-RECV</text>
<rect x="140" y="34" width="84" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="182.0" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全连接队列</text>
<text x="182.0" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等 accept</text>
<rect x="240" y="34" width="84" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.0" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用</text>
<text x="282.0" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">accept()</text>
<line x1="124" y1="56" x2="140" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="140.0,56.0 133.0,59.2 133.0,52.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="224" y1="56" x2="240" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="240.0,56.0 233.0,59.2 233.0,52.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">半连接：回了 SYN+ACK，等第三次 ACK</text>
<text x="8" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">全连接：握手完成，等应用 accept</text>
<text x="8" y="152" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">攻击：伪造源 IP 的 SYN 塞满半连接队列</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 正常用户的 SYN 被丢弃</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">SYN cookies：队列满时不存状态，</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">信息编进 SYN+ACK 的序列号</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Recv-Q 接近 Send-Q：accept 太慢</text>
</svg>
SYN 先进半连接队列，收到第三次 ACK 后进全连接队列，最后被应用 `accept`；攻击塞满第一个队列。`ss -lnt` 监听状态下 Recv-Q 是全连接队列当前排队数，Send-Q 是上限，Recv-Q 接近 Send-Q 说明 `accept` 太慢，那是另一个队列的问题。
**业务场景。** 边缘节点收到大量伪造源 IP 的 SYN，真实用户连不上，封 IP 封掉一个又来一个；开 SYN cookies 加入口清洗后恢复。
**容易错。**
- **以为按 IP 封禁能挡。**
- **调大一个参数就以为队列大了：** 三处取最小。
- **混淆两个队列：** 一个等第三次 ACK，一个等应用 accept。
