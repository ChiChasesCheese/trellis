---
id: traffic-gateway-buffering
node: traffic.gateways
type: qa
---
## Q
Reverse-proxy request/response buffering — what does it protect upstream from, and when must you turn it off?

## A
The proxy absorbs a slow client's upload fully, then forwards to the upstream at LAN speed; responses likewise: upstream hands off the full response in milliseconds and the proxy drip-feeds it. Upstream workers stop being held hostage by slow or malicious clients (slowloris-style connection exhaustion).

Turn it off when incremental delivery *is* the product:

- **SSE / streamed responses** — buffering holds events until the response completes (`X-Accel-Buffering: no` / `proxy_buffering off`).
- **Large uploads** — buffering doubles them into proxy disk/memory.
- WebSockets bypass buffering after the upgrade anyway.

## Q zh
反向代理请求/响应缓冲 — 它保护上游免于什么，什么时候必须关闭它？

## A zh
代理完全吸收缓慢客户端的上传，然后以 LAN 速度转发到上游；响应同样：上游在毫秒内交出完整响应，代理滴流供给它。上游工作人员停止被缓慢或恶意客户端所阻挠（slowloris 风格的连接耗尽）。

当增量交付*是*产品时关闭它：

- **SSE / 流响应** — 缓冲持有事件直到响应完成（`X-Accel-Buffering: no` / `proxy_buffering off`）。
- **大上传** — 缓冲使它们加倍到代理磁盘/内存。
- WebSocket 升级后无论如何都绕过缓冲。
