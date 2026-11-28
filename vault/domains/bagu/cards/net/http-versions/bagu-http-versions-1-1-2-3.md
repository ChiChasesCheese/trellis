---
id: bagu-http-versions-1-1-2-3
node: b.net.http-versions
type: qa
step: 1
---
## Q
**HTTP/1.1、2、3 · 各解决了什么**｜追问

面试官：「HTTP/1.1、HTTP/2、HTTP/3 有什么区别？短视频列表一次加载几十张封面，为什么 HTTP/2 更合适？」

## A
**基本回答。** 1.1 引入持久连接（keep-alive），但同一连接请求串行，有应用层队头阻塞，浏览器对同一域名开约 6 个连接。2 用二进制分帧加多路复用：请求和响应拆成带流 ID 的帧，一个 TCP 连接上并发交错，接收方按流 ID 重组；另有头部压缩（HPACK）。但所有流共用一个 TCP 连接，丢一个包后面已到的数据也要等重传，所有流被卡。3 基于 QUIC（UDP），流之间互不阻塞，握手更快，代价是 UDP 可能被限、CPU 开销更大。
**2026 亮点。** 面向用户的 CDN 和边缘开 HTTP/3（nginx 1.25 起支持），客户端首次走 TCP，靠 `Alt-Svc` 响应头或 DNS HTTPS 记录发现 h3，失败回退 HTTP/2；机房内部低丢包链路继续用 HTTP/2 的 gRPC。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">HTTP/1.1：同一连接上请求串行</text>
<rect x="8" y="24" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求 1</text>
<line x1="88" y1="37" x2="118" y2="37" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,37.0 111.6,39.9 111.6,34.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="24" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="158.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求 2</text>
<line x1="198" y1="37" x2="228" y2="37" stroke-width="1.2" stroke="currentColor"/>
<polygon points="228.0,37.0 221.6,39.9 221.6,34.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="228" y="24" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="268.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求 3</text>
<text x="10" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所以浏览器对同一域名开约 6 个连接</text>
<text x="10" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">HTTP/2：一个 TCP 连接，多流的帧交错</text>
<rect x="8" y="102" width="50" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="33.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 1</text>
<rect x="62" y="102" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 2</text>
<rect x="116" y="102" width="50" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="141.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 1</text>
<rect x="170" y="102" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="195.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 3</text>
<rect x="224" y="102" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="249.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 2</text>
<rect x="278" y="102" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="303.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 3</text>
<text x="10" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按流 ID 重组；但 TCP 丢一个包，所有流都卡</text>
<text x="10" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">HTTP/3：跑在 QUIC 上，流之间互不阻塞</text>
<rect x="8" y="180" width="100" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="58.0" y="197.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 1 正常</text>
<rect x="116" y="180" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="166.0" y="197.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 2 等重传</text>
<rect x="224" y="180" width="100" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="274.0" y="197.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流 3 正常</text>
<text x="10" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">握手更快；代价：UDP 可能被限，CPU 开销大</text>
</svg>
1.1 同一连接串行；2 一个连接里帧交错，但 TCP 丢包卡全部流；3 每个流独立，只有丢包的那个等重传。
**业务场景。** 短视频列表一次加载 30 张封面：1.1 约 6 个连接，分约 5 批排队（简化估算）；2 在一个连接上同时发 30 个请求，帧交错到达；弱网丢一个包，2 下 30 张图都被拖慢，3 下只影响丢包所属的那个流。
**容易错。**
- **以为 HTTP/2 彻底解决队头阻塞：** 只解决应用层，TCP 层丢包仍卡所有流。
- **以为 HTTP/3 总是更快：** 弱网丢包时收益才明显。
- **混淆 502 和 504：** 502 是上游返回坏响应或连接被拒、崩溃（查上游进程是否崩溃、keep-alive 超时是否比网关短）；504 是上游没在时间内响应（查上游是否太慢、网关超时是否太短）。
