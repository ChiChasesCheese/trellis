---
id: bagu-websocket-push-3-sse-vs-ws
node: a.net.websocket-push
type: qa
step: 3
---
## Q
**SSE 与 WebSocket · 怎么选**｜必会

面试官：「SSE 和 WebSocket 都能推送，你怎么选？」

## A
**基本回答。** 看客户端要不要高频上行。SSE 是一次很长的 HTTP 下载（`text/event-stream`），单向、只传文本，代理、鉴权、监控都按 HTTP 处理；浏览器自带断线重连，重连带 `Last-Event-ID` 请求头，服务端据此续传（前提是给事件设 ID 并保留最近一段）。WebSocket 全双工、支持二进制、延迟最低，但要网关支持升级，重连和心跳自己做。只推通知、状态、行情、AI 流式回复用 SSE；游戏、聊天、弹幕收发用 WebSocket。HTTP/1.1 下浏览器对同一域名并发连接通常 6 个，多个 SSE 标签页会占满，HTTP/2 基本不受影响。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="56" y="4" width="138" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="125" y="21" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SSE</text>
<rect x="198" y="4" width="138" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="267" y="21" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">WebSocket</text>
<text x="4" y="55" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">方向</text>
<rect x="56" y="36" width="138" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务端→客户端</text>
<rect x="198" y="36" width="138" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="267" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">双向全双工</text>
<text x="4" y="89" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">内容</text>
<rect x="56" y="70" width="138" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只传文本</text>
<rect x="198" y="70" width="138" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="267" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">文本和二进制</text>
<text x="4" y="127" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重连</text>
<rect x="56" y="104" width="138" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器自带</text>
<text x="125" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Last-Event-ID 续传</text>
<rect x="198" y="104" width="138" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="267" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要自己做</text>
<text x="267" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重连和心跳</text>
<text x="4" y="169" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">底座</text>
<rect x="56" y="146" width="138" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">普通 HTTP</text>
<rect x="198" y="146" width="138" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="267" y="161" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">升级协议</text>
<text x="267" y="177" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关要支持</text>
<text x="4" y="211" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">适合</text>
<rect x="56" y="188" width="138" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125" y="203" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知·行情</text>
<text x="125" y="219" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">AI 流式回复</text>
<rect x="198" y="188" width="138" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="267" y="203" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">游戏·聊天</text>
<text x="267" y="219" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">弹幕收发</text>
<text x="4" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SSE 就是一次很长的 HTTP 下载</text>
</svg>
逐行对比：方向、内容、重连、底座、适合场景；最关键是只推不收选 SSE。
**业务场景。** AI 助手回复逐字显示：用户发一次普通请求，服务端回 `text/event-stream` 并保持不关，模型每生成一小段写一个事件；中途断网浏览器带最后事件 ID 重连续传；整个过程只有下行，不必部署一套 WebSocket 网关。
**容易错。**
- **以为 SSE 是 WebSocket 低配版：** 只推不收时 SSE 更简单、运维更省。
- **以为 SSE 能传二进制：** 要先编码成文本，或改用 WebSocket。
