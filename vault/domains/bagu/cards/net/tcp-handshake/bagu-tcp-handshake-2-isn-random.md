---
id: bagu-tcp-handshake-2-isn-random
node: a.net.tcp-handshake
type: qa
step: 2
---
## Q
**TCP 握手 · 初始序列号为什么要随机**｜追问

面试官：「每次建立连接，初始序列号为什么不能固定从 0 开始？」

## A
**基本回答。** 序列号给字节流编号，接收方据此确认、乱序重组、去重，发送方据此判断重传。ISN 随机有两个目的：一是防旧连接滞留的延迟报文被相同四元组（源 IP、源端口、目的 IP、目的端口）的新连接误收；二是防攻击者猜序列号伪造报文（只有落在窗口内的序列号才被接收）。实现是「时钟递增值加四元组与密钥的哈希」：RFC 建议约每 4 微秒加一，Linux 约每 64 纳秒，保证同四元组的新连接大概率落在旧连接之后，哈希保证不可预测。序列号 32 位会回绕。TIME_WAIT 等旧报文过期，ISN 保证残留的也难混淆，两者配合。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧连接的迟到包 seq=1000，新连接用同一四元组</text>
<text x="8" y="40" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">固定 ISN：新连接也从 1000 附近起</text>
<rect x="60" y="50" width="150" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="135.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新连接的窗口</text>
<line x1="110" y1="112" x2="110" y2="78" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="110.0,78.0 113.2,85.0 106.8,85.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="122" y="102" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">旧包落进窗口，被收下</text>
<text x="8" y="144" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">随机 ISN：新连接从 7777 起</text>
<rect x="180" y="154" width="140" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="250.0" y="172.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新连接的窗口</text>
<line x1="110" y1="214" x2="110" y2="182" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="110.0,182.0 113.2,189.0 106.8,189.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="122" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">窗口外，直接丢弃</text>
<text x="8" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ISN = 时钟计数 + hash(四元组, 密钥)</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时钟 RFC 约 4 微秒、Linux 约 64 纳秒加一</text>
</svg>
上排固定 ISN，旧包落进新窗口被当成合法数据；下排随机 ISN，新窗口远离旧包，旧包被丢弃。
**业务场景。** 玩家手机在地铁断网后很快用同一个源端口重连，四元组与旧连接相同：固定 ISN 下旧连接滞留的 seq=1000 的包落进新窗口，被当成对局数据造成状态错乱；新连接从 7777 起步，旧包落在窗口外被丢弃。
**容易错。**
- **以为从 0 开始最规矩：** 旧包串线，也易被猜。
- **以为 ISN 是纯随机数。**
- **以为有了随机 ISN 就不需要 TIME_WAIT。**
