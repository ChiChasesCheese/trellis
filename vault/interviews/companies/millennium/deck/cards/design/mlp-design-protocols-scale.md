---
id: mlp-design-protocols-scale
node: design.protocols
step: 2
type: qa
---
## Q
**客户端与服务之间用什么协议通信：规模变大后**｜设计轮

用户和请求量涨了几十倍，原来的选择会在哪里出问题，怎么调整？

## A
```mermaid
%%{init: {"flowchart": {"wrappingWidth": 320}, "themeVariables": {"fontSize": "18px"}}}%%
flowchart LR
  C["百万客户端"] --> G["网关与负载均衡"]
  G --> P["推送服务器组"]
  G --> A["API 服务器组"]
  A --> Q["消息队列"]
  Q --> P
```

- **REST 的瓶颈：** 请求量大了，最先做的是无状态化加水平扩展，前面放负载均衡；读多的接口加缓存（CDN 或 Redis）；写多的接口用批量请求，或者改成先进队列再处理，把峰值摊平。
- **内部调用换成 gRPC：** 服务之间调用多到序列化和头部成为开销时，换二进制和多路复用能降延迟和带宽；同时要加超时、重试和熔断（circuit breaker，下游连续失败就暂时不再调用），避免一个慢服务拖垮上游。
- **WebSocket 的瓶颈是连接数：** 每个连接占内存和文件描述符，一台机器能撑的连接数有限；服务器要横向扩展，负载均衡按连接粘性分发。推送服务器组和业务服务器分开，由消息队列或发布订阅（pub/sub，按主题广播）把消息送到持有该用户连接的那台机器。
- **断线重连和补数据：** 规模大了，网络抖动是常态，重连会同时涌来（惊群，thundering herd），客户端重连要加随机退避；每条推送带单调递增的序号，重连时报告最后收到的序号，服务端补发缺失的部分。
- **消息队列的取舍：** 吞吐靠分区（partition）横向扩展，同一个分区内保持顺序，所以要保序的消息用同一个键（如 symbol）放进同一个分区；投递一般是"至少一次"，消费者要幂等（同一条处理两次结果不变）；消费者落后要有监控和报警。
- **慢客户端：** 推送给慢的消费者时，不能让它拖住整条推送链路；给每个连接设有界缓冲，满了就丢弃旧数据（行情）或断开连接重新同步。

**英文答法。**
- "At scale, WebSocket is limited by **connection count**, so I split push servers from API servers and route messages by a **pub/sub** layer."
- "Every push carries a **sequence number**, so a reconnecting client can ask for what it missed."
- "Queue consumers must be **idempotent**, because delivery is at-least-once."
