---
id: bagu-websocket-push-2-ws-handshake
node: a.net.websocket-push
type: qa
step: 2
---
## Q
**WebSocket 握手 · 与 HTTP 是什么关系**｜必会

面试官：「WebSocket 连接是怎么建立的？它和 HTTP 是什么关系？」

## A
**基本回答。** 先发普通 HTTP/1.1 `GET`，带 `Upgrade: websocket`、`Connection: Upgrade`、随机 `Sec-WebSocket-Key`、`Sec-WebSocket-Version: 13`；服务端同意回 `101 Switching Protocols` 加 `Sec-WebSocket-Accept`，此后同一条 TCP 改用 WebSocket 帧双向收发。借 HTTP 是为了复用 80 和 443、穿过现有代理防火墙和负载均衡，并能用 Cookie 或 Token 在握手请求里鉴权。`Accept` = Base64(SHA-1(Key + 固定 GUID `258EAFA5-E914-47DA-95CA-C5AB0DC85B11`))，只证明服务端理解 WebSocket，不是认证（规范示例 Key `dGhlIHNhbXBsZSBub25jZQ==` 对应 Accept `s3pPLMBiTxaQ9kYGzzhZRbK+xOo=`）。线上用 `wss://`，并发心跳 ping/pong 发现断连、防空闲被关。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 224">
<text x="4" y="13" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">还在 HTTP/1.1 上：请求头带随机 Key</text>
<rect x="18" y="18" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="33" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端</text>
<line x1="54" y1="40" x2="54" y2="182" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="250" y="18" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="286" y="33" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务端</text>
<line x1="286" y1="40" x2="286" y2="182" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="58" y1="60" x2="282" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,60.0 275.0,63.2 275.0,56.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">GET + Upgrade: websocket</text>
<line x1="282" y1="94" x2="58" y2="94" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="58.0,94.0 65.0,90.8 65.0,97.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">101 + Sec-WebSocket-Accept</text>
<line x1="58" y1="128" x2="282" y2="128" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,128.0 275.0,131.2 275.0,124.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="123" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">WebSocket 帧</text>
<line x1="282" y1="162" x2="58" y2="162" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="58.0,162.0 65.0,158.8 65.0,165.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="157" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">WebSocket 帧（服务端随时推）</text>
<text x="4" y="205" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Accept = Base64(SHA-1(Key + 固定 GUID))</text>
<text x="4" y="221" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">握手后同一条 TCP 不再是 HTTP</text>
</svg>
前两条箭头是握手，仍是一次 HTTP 请求响应；之后全是 WebSocket 帧，服务端不用等请求就能推。
**业务场景。** 直播间 WebSocket 经 Nginx 后每隔约 60 秒断线：`proxy_read_timeout` 默认 60 秒，一时没人发弹幕连接空闲就被关。修复：客户端每 30 秒发 ping、服务端回 pong 重置计时，按需调大 `proxy_read_timeout`，并确认 Nginx 透传 `Upgrade` 和 `Connection` 头，否则握手就失败。
**容易错。**
- **把 Accept 当身份认证：** 鉴权靠 Cookie、Token。
- **用 ws:// 上线：** 明文可被窥探改写。
- **不发心跳：** 对端消失本端发现不了。
