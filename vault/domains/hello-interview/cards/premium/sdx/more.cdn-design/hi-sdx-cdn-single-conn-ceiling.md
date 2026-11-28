---
id: hi-sdx-cdn-single-conn-ceiling
node: more.cdn-design
type: qa
step: 3
---
## Q
**大文件下载：单连接为什么跑不满，并行为什么有效**｜补充 · 内容分发网络（CDN）设计 · 加分

面试官：「用户经 CDN 下载大文件，往返时延 40 ms，链路 100 Mbps。为什么单条 TCP 连接常常跑不满？把文件拆成多段、用 Range 请求并行下载为什么能更快？有什么上限？」

## A
**结论。** 单连接速度受 窗口 ÷ RTT 限制，丢包会把它压得更低，与链路带宽无关；多条连接各有独立的拥塞窗口，加起来逼近链路带宽，但不会超过它。CDN 必须支持从缓存对象回字节范围。

**要点。**
- **管道容量：** 100 Mbps × 40 ms = 4 Mb = 500 KB。窗口小于它就填不满，比如 64 KB 窗口只有 64KB×8 ÷ 0.04 s ≈ 13 Mbps。
- **丢包：** 稳态近似为 1.22 × MSS ÷ (RTT × √丢包率)。MSS 1460 B、RTT 40 ms、丢包 0.1% 时约 11 Mbps。
- **并行：** 8 条连接各约 11 Mbps，合计约 90 Mbps，接近 100 Mbps 上限；再多连接只是互相挤占。
- **做法：** 每段发 `Range: bytes=…`，各用一条连接，客户端拼装；CDN 缓存要能回部分范围。
- **代价：** 客户端更复杂，请求数乘以段数，也占用更多共享带宽；小文件不值得。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="10" y="22" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">单条连接（丢包 0.1%）≈ 11 Mbps</text>
<rect x="10" y="28" width="22" height="12" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="10" y="64" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">8 条并行 ≈ 90 Mbps</text>
<rect x="10" y="70" width="180" height="12" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="10" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">链路上限 100 Mbps</text>
<rect x="10" y="112" width="200" height="12" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="10" y="152" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">速度 ≈ 1.22 × MSS ÷ (RTT × √丢包率)</text>
<text x="10" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">MSS 1460 B，RTT 40 ms</text>
</svg>

**面试里这样说。** 「单连接速度是窗口除以 RTT，丢包还会把它压到十几 Mbps。拆成 8 段并行，每条连接各有窗口，合计接近链路带宽。前提是 CDN 能从缓存回字节范围；但并行不会超过链路上限。」

**易错。**
- **以为并行能超过链路带宽：** 100 Mbps 的链路上，多少条连接加起来都不会超过 100 Mbps。
- **不确认 CDN 支持范围请求：** 每段都变成整对象回源。
