---
id: networking-sse-mechanics
node: networking.realtime
type: qa
---
## Q
Two built-in SSE features that you'd otherwise hand-build on raw WebSockets?

## A
- **Automatic reconnection with resume**: browsers reconnect on drop and send the last received event id in `Last-Event-ID`, so the server can replay what was missed.
- **Plain HTTP transport**: works through proxies, LBs, and HTTP/2 multiplexing with normal auth headers — no protocol upgrade, no special infra.

Limits to state alongside: one direction only (server→client), text frames only.

## Q zh
两个内置 SSE 特性，否则你会在原始 WebSocket 上手工构建？

## A zh
- **自动重连接带恢复**：浏览器在下降时重连并在 `Last-Event-ID` 中发送最后接收的事件 id，所以服务器可以重放丢失的内容。
- **普通 HTTP 传输**：通过代理、LB 和 HTTP/2 多路复用工作带正常身份验证头 — 没有协议升级、没有特殊基础设施。

限制旁边的状态：单向（服务器→客户端）、仅文本帧。
