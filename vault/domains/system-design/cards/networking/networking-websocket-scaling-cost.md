---
id: networking-websocket-scaling-cost
node: networking.realtime
type: qa
---
## Q
What makes a WebSocket fleet fundamentally harder to scale than a stateless HTTP fleet? Name the three concrete problems.

## A
**Connection state lives on a specific server.**

- **Routing**: to push to user X you must find *which* server holds X's socket → needs a connection registry (e.g. Redis) or a pub/sub layer every server subscribes to.
- **Deploys/drains**: restarting a server drops every connection it holds; clients must reconnect and resync missed state.
- **Reconnect storms**: an LB or server failure makes tens of thousands of clients reconnect at once — require jittered exponential backoff clientside.

## Q zh
什么使 WebSocket 舰队比无状态 HTTP 舰队更难扩展？命名三个具体问题。

## A zh
**连接状态存在于特定服务器。**

- **路由**：向用户 X 推送你必须找到*哪个*服务器持有 X 的套接字 → 需要连接注册表（例如 Redis）或每个服务器订阅的 pub/sub 层。
- **部署/排空**：重启一个服务器删除它持有的每个连接；客户端必须重连并重新同步错过的状态。
- **重连风暴**：LB 或服务器故障使数万个客户端一次重连 — 需要客户端侧的抖动指数退避。
