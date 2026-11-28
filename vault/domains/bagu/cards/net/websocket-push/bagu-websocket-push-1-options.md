---
id: bagu-websocket-push-1-options
node: a.net.websocket-push
type: qa
step: 1
---
## Q
**服务端推送 · 有哪些方案、怎么取舍**｜必会

面试官：「服务端要主动把消息送到用户的浏览器或 App，有哪些方案？怎么选？」

## A
**基本回答。** HTTP 是客户端问、服务端答，服务端没有主动开口的机会。四种方案：短轮询（定时问，多数返回「没有」，延迟取决于间隔，间隔短请求量大、间隔长消息慢，两头牵制）；长轮询（服务端挂住请求，有数据或超时才返回，客户端立刻再发，延迟低、空请求少，但每个挂起请求占一个连接，必须设超时，否则被代理悄悄断开；Nacos、Apollo 配置中心和 Kafka、RocketMQ 消费拉取都在用）；SSE（一条 HTTP 长响应，服务端单向写文本事件）；WebSocket（升级后的全双工长连接，支持二进制）。选择：要双向实时用 WebSocket，只要服务端单向推用 SSE，旧环境兜底用长轮询，更新很少的场景轮询更简单。推送要服务端维护有状态的长连接，连接数、心跳、重连都要管。iframe 流已淘汰。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 258">
<text x="4" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">短轮询</text>
<rect x="76" y="4" width="18" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="118" y="4" width="18" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="160" y="4" width="18" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="202" y="4" width="18" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="244" y="4" width="18" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="286" y="4" width="18" height="18" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="76" y="44" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">定时问，多数返回「没有」</text>
<text x="4" y="74" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">长轮询</text>
<rect x="76" y="58" width="120" height="18" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="136" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">挂住等待</text>
<rect x="198" y="58" width="22" height="18" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="209" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有</text>
<rect x="222" y="58" width="90" height="18" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="267" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">立刻再发</text>
<text x="76" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">有数据或超时才返回</text>
<text x="4" y="128" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SSE</text>
<rect x="76" y="112" width="258" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="96" y="115" width="12" height="12" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="150" y="115" width="12" height="12" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="222" y="115" width="12" height="12" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="290" y="115" width="12" height="12" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="76" y="152" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一条 HTTP 长响应，服务端单向写事件</text>
<text x="4" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">WebSocket</text>
<line x1="76" y1="171" x2="326" y2="171" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="326.0,171.0 319.0,174.2 319.0,167.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="326" y1="183" x2="76" y2="183" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="76.0,183.0 83.0,179.8 83.0,186.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="76" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">升级后的长连接，双方随时发</text>
<text x="4" y="230" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">前两种是客户端拉，后两种是服务端推</text>
</svg>
前两行是客户端拉，后两行是服务端推；空心方块是「问了但没有」。
**业务场景。** 站内信小红点，100 万人在线：短轮询每秒查一次就是每秒 100 万次请求，绝大多数返回「没有」；长轮询请求挂着，30 秒超时才重发，但服务端要同时挂 100 万个请求；SSE 或 WebSocket 只在有消息时才有流量，如果还要聊天（上行发消息）只能选 WebSocket。
**容易错。**
- **以为长轮询就是把短轮询间隔调短。**
- **以为 SSE 和 WebSocket 差不多：** SSE 单向文本走普通 HTTP，WebSocket 双向且需升级协议。
- **以为推送一定比轮询好。**
