---
id: storage-dataflow-modes
node: storage.encoding
type: qa
---
## Q
DDIA names three modes by which encoded data flows between processes. Name all three, and for each, say who the reader is and which compatibility direction that forces you to maintain.

## A
- **Through a database** — the reader is *a future process*, possibly years away: "sending a message to your future self." Forces **backward** compatibility across every schema version ever written (data outlives code). During rollouts it needs forward compatibility too, since old code may read rows new code just wrote.
- **Through service calls (REST/RPC)** — the reader is *the other side of a live request*, and servers and clients upgrade independently (rolling deploys, mobile clients you can't force-update). Forces **both directions at once**: new servers read old clients' requests, old clients read new servers' responses.
- **Through async messages (broker/queue)** — like RPC but decoupled in time, with **multiple independent consumers** of one topic. Forces both directions, made stricter by fan-out (each consumer upgrades on its own schedule) and by **replay**: reprocessing a topic means today's code reading arbitrarily old messages.

Value of the taxonomy: "who will read these bytes, and when?" is the question that tells you which compatibility rules you're actually signing up for.

## Q zh
DDIA 列出编码后的数据在进程之间流动的三种模式。说出全部三种，并对每一种说明读者是谁、这迫使你维护哪个方向的兼容性。

## A zh
- **经由数据库** — 读者是*未来的某个进程*，可能在几年之后："给未来的自己发消息"。迫使你对历史上写入过的每个 schema 版本保持 **backward** 兼容（数据比代码活得久）。滚动发布期间还需要 forward 兼容，因为旧代码可能读到新代码刚写的行。
- **经由服务调用（REST/RPC）** — 读者是*一次在线请求的对端*，而服务端和客户端独立升级（滚动部署、无法强制更新的移动客户端）。迫使你**同时维护两个方向**：新服务端读旧客户端的请求，旧客户端读新服务端的响应。
- **经由异步消息（broker/队列）** — 类似 RPC 但在时间上解耦，且一个 topic 有**多个独立消费者**。两个方向都要，而且被扇出（每个消费者按自己的节奏升级）和**重放（replay）**收得更紧：重新处理一个 topic 意味着今天的代码要读任意旧的消息。

这套分类的价值："这些字节会被谁、在什么时候读？"正是告诉你实际要签下哪些兼容性规则的那个问题。
