---
id: networking-tcp-vs-udp
node: networking.protocols
type: qa
---
## Q
When is UDP the right transport despite giving up TCP's guarantees? Name the guarantees you're dropping and two workloads that want that.

## A
Dropping: **ordering, retransmission, and connection state** — which means no head-of-line blocking and no handshake/teardown cost.

- **Live media / voice / games**: a late packet is worthless; retransmitting old data adds latency for nothing.
- **Protocols that reimplement reliability themselves**: DNS lookups (single tiny request/response), and **QUIC**, which builds TLS + streams + loss recovery on UDP to escape TCP's kernel-level head-of-line blocking.

## Q zh
什么时候 UDP 是正确的传输尽管放弃 TCP 的保证？命名你放弃的保证和两个想要那个的工作负载。

## A zh
放弃：**排序、重传和连接状态** — 这意味着没有行首阻塞、没有握手/拆除成本。

- **直播媒体/语音/游戏**：一个晚包是无价值的；重传旧数据为没有添加延迟。
- **重新实现可靠性的协议**：DNS 查询（单一小请求/响应），和 **QUIC**，在 UDP 上构建 TLS + 流 + 丢失恢复以逃脱 TCP 的内核级行首阻塞。
