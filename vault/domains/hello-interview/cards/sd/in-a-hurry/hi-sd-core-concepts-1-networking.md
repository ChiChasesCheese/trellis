---
id: hi-sd-core-concepts-1-networking
node: sd.in-a-hurry.core-concepts
type: qa
step: 1
---
## Q
**网络：协议、实时推送与负载均衡的默认选择**｜系统设计 · 速览

系统设计面试里，网络层面应当记住哪些默认选择？WebSocket、SSE、gRPC、L4 与 L7 负载均衡分别什么时候用？

## A
**要点。**

- 默认 HTTP over TCP，覆盖约 90% 的场景。
- 实时更新：SSE（Server-Sent Events）是单向的，客户端发一次 HTTP 请求后由服务端持续下推（比分、通知）；WebSocket 是双向的（聊天、协同编辑）。两者都是有状态连接，不能直接丢给普通负载均衡，要考虑连接保持与服务器宕机时大量连接的恢复。
- gRPC：二进制序列化加 HTTP/2，适合内部服务间对性能敏感的调用；浏览器原生不支持，所以通常是对外 REST、对内 gRPC。
- 负载均衡：L7 看请求内容，可按路径把 API 和网页分到不同服务；L4 只在 TCP 层分发连接，更快但更「傻」，WebSocket 这种长连接通常用 L4。

**易错。** 只要提到「实时」就上 WebSocket；长轮询或 SSE 够用时，WebSocket 的有状态复杂度不值得。

**数字。** 纽约到伦敦单程光纤延迟下限约 80 ms，所以全球低延迟要靠区域部署和 CDN。
