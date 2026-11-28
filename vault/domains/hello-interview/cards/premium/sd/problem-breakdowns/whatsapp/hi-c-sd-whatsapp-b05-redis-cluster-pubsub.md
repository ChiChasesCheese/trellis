---
id: hi-c-sd-whatsapp-b05-redis-cluster-pubsub
node: sd.problem-breakdowns.whatsapp.beyond
type: qa
step: 5
---
## Q
**WhatsApp 即时通讯 · Redis 集群里 Pub/Sub 其实不能线性扩展**｜拓展 · 加分

把 Pub/Sub 频道"按 userId 分片到 Redis 集群"，在 Redis Cluster 里真的能线性扩展吗？

## A
- **经典 Pub/Sub 在集群里是广播的：** Redis Cluster 中的 `PUBLISH` 会通过集群总线转发给所有节点（包括没有任何订阅者的节点），节点收到后再投递给自己的订阅者。每条消息的网络开销随节点数增长，加节点反而放大消息总线的流量，不是线性扩展。Redis 7.0 新增的分片 Pub/Sub 才改变了这一点，经典 `PUBLISH` 的行为没有变。
- **两种解法：**
  - 分片 Pub/Sub（Redis 7.0 引入 `SPUBLISH` / `SSUBSCRIBE`）：频道按哈希槽归属某个分片，消息只在该分片内传播；
  - 不用 Cluster 模式，在客户端或代理层按 userId 做一致性哈希，选择多个互相独立的 Redis 实例，每个实例只管自己那部分频道。
- **后果：** 聊天服务器订阅某用户频道时要先算出它属于哪个实例或分片，所以每台聊天服务器要与每个分片（或实例）都保持连接。
- **口述方式：** 说"按 userId 分片"后，被追问就补一句"用分片 Pub/Sub 或客户端哈希，不用广播式的集群 Pub/Sub"，显出你知道实现细节。
- **模式。** 把分片键放到客户端：当中间层不能路由时，让调用方先算分片再连接。
