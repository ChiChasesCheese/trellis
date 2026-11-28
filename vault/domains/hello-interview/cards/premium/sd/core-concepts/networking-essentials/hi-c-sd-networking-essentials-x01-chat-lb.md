---
id: hi-c-sd-networking-essentials-x01-chat-lb
node: sd.core-concepts.networking-essentials.exam
type: qa
step: 1
---
## Q
**网络基础 · 聊天室的负载均衡怎么选**｜考点 · 必会

聊天服务用 WebSocket，要部署多台服务器。负载均衡用 L4 还是 L7，调度算法选什么？

## A
- **L4：** WebSocket 是持久连接，L4 把整条 TCP 连接固定到同一台服务器，快且开销小。有的 L7 也支持 WebSocket，但一般 L4 更合适。
- **算法：** 最少连接，避免某台服务器逐渐积累大部分长连接；轮询对长连接会失衡，因为连接寿命长短不一。
- **配套：** 健康检查摘除故障节点；均衡器本身用 DNS 轮转多台避免单点。
- **资深加分：** 新服务器加入时，已有连接不会自动迁移，新连接才会过去；扩容后短期仍可能不均衡，要有重连或排空策略。
- **反例：** 普通 HTTP 接口、长轮询用 L7，可按 URL 和 Cookie 路由。
