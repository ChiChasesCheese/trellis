---
id: hi-c-sd-core-concepts-n02-networking
node: sd.in-a-hurry.core-concepts.notes
type: qa
step: 2
---
## Q
**核心概念速览 · 网络：协议、实时推送与负载均衡**｜摘要 · 必会
网络部分有哪些默认选择？SSE 与 WebSocket、L4 与 L7 负载均衡各什么时候用？

## A
- **默认：** HTTP over TCP，覆盖约 90% 的场景，面试官默认你这样用。
- **实时更新：** SSE（Server-Sent Events）单向，客户端发一次 HTTP 请求打开连接后，由服务器持续下推（比分、通知），简单且更契合标准 HTTP 基础设施；WebSocket 双向，双方随时发消息（聊天、协同编辑），客户端需要频繁向服务器推送时才必要。两者都是有状态的连接，不能直接扔到普通负载均衡后面，要考虑连接保持，以及服务器宕机时大量连接怎么恢复。
- **gRPC：** 二进制序列化加 HTTP/2，比 JSON over HTTP 快得多，适合性能关键的内部服务调用；浏览器原生不支持（gRPC-Web 要代理且功能不全），所以对外 REST、对内 gRPC。
- **负载均衡：** L7 在应用层，能看 HTTP 内容，可按路径把 API 和网页请求分到不同服务；L4 在 TCP 层，更快但"更傻"，只分发连接。WebSocket 这类长连接通常用 L4。
- **易错：** 提到"实时"就上 WebSocket；长轮询或 SSE 够用时，WebSocket 的有状态复杂度不值得。
- **地理：** 纽约到伦敦单程光纤延迟下限约 80 毫秒，全球低延迟需要区域部署与数据按地理复制或分区；CDN 就是为此存在。
