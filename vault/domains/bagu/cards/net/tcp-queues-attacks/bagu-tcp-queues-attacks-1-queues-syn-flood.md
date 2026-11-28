---
id: bagu-tcp-queues-attacks-1-queues-syn-flood
node: b.net.tcp-queues-attacks
type: qa
step: 1
---
## Q
**半连接与全连接队列 · 溢出、SYN 攻击与连接数上限**｜追问

面试官：「大促时客户端大量连接超时，服务端 CPU 却不高。TCP 半连接队列和全连接队列是什么，满了会怎样？SYN 攻击怎么防？单机最多能撑多少连接？」

## A
**基本回答。** 收到 SYN 后连接先进半连接队列（SYN_RCV，等第三次握手）；第三次 ACK 到达，握手完成，转进全连接队列（ESTABLISHED），等应用 `accept()` 取走。全连接队列上限 `min(somaxconn, backlog)`（`net.core.somaxconn` 与 `listen()` 传的参数取小；实测 `listen(2)` 不 `accept` 时前 3 个连接成功，第 4 个超时）。队列满时由 `tcp_abort_on_overflow` 决定：默认 0 丢最后那个 ACK，客户端以为已连上、发数据一直重传、最终超时才暴露；设 1 回 RST，客户端报 `connection reset by peer`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<rect x="10" y="8" width="190" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端发出 SYN</text>
<line x1="105" y1="36" x2="105.0" y2="55.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="105,62 101.8,55.0 108.2,55.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="62" width="190" height="46" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="81.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">半连接队列</text>
<text x="105" y="96.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SYN_RCV，等第三次握手</text>
<text x="212" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SYN Flood</text>
<text x="212" y="94" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只发 SYN，把这里占满</text>
<line x1="105" y1="108" x2="105.0" y2="139.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="105,146 101.8,139.0 108.2,139.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="113" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第三次 ACK 到达</text>
<rect x="10" y="146" width="190" height="46" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="105" y="165.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全连接队列</text>
<text x="105" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ESTABLISHED，等 accept</text>
<text x="212" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">队列满了：</text>
<text x="212" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">丢 ACK 或回 RST</text>
<text x="212" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">上限 min(somaxconn,</text>
<text x="212" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">backlog)</text>
<line x1="105" y1="192" x2="105.0" y2="225.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="105,232 101.8,225.0 108.2,225.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="113" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">应用调用 accept()</text>
<rect x="10" y="232" width="190" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="250" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用拿到这条连接</text>
</svg>
连接先停半连接队列，第三次握手后进全连接队列，`accept()` 后应用才拿到；SYN Flood 占满前者，应用 `accept` 慢填满后者。`ss -lnt` 看 Recv-Q 是否接近 Send-Q，`netstat -s | grep -i overflow` 看累计溢出次数。
**SYN 攻击与连接数。** SYN Flood 只发 SYN 不回第三次 ACK，占满半连接队列；源地址伪造，封 IP 无效。防御：`tcp_syncookies=1`（状态编进 SYN+ACK 序列号，新内核默认开）、调大 `tcp_max_syn_backlog`、减少 `tcp_synack_retries`、边缘限速或高防。单机连接数能超过 65535：连接由四元组标识，65535 只限制同一源地址对同一目标的端口数，真正上限是文件描述符、内存和 CPU。
**业务场景。** 大促开场客户端大量连接超时但服务端 CPU 不高：`ss -lnt` 显示 Recv-Q 顶着 Send-Q，overflow 计数在涨，是全连接队列溢出。短期调大 `backlog` 和 `somaxconn` 争取缓冲，同时查应用 `accept` 为什么慢（线程被打满、阻塞的初始化）。
**容易错。**
- **CPU 不高就认为没问题：** 根因是没人来 `accept`。
- **只调大 backlog：** 队列只是缓冲，只会推迟溢出。
- **把 65535 当单机连接数上限。**
