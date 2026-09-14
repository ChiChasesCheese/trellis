---
id: networking-realtime-backpressure
node: networking.realtime
type: qa
---
## Q
One WebSocket client on a bad network can't keep up with your push rate. What builds up where, and what are the three standard policies?

## A
The client's TCP receive window fills, the server's kernel send buffer fills, then the **per-connection application queue grows unbounded** — a handful of slow consumers can exhaust server memory.

- **Drop** oldest/newest — fine when messages are independent.
- **Coalesce** — keep only the latest value per key (tickers, presence, cursors): ideal when messages are snapshots, not deltas.
- **Disconnect** past a queue threshold — client reconnects and resyncs from source of truth.

Choose by semantics: deltas require either reliable delivery or resync-on-gap; snapshots can always coalesce.

## Q zh
一个坏网络上的 WebSocket 客户端无法跟上你的推送率。在哪里建立，三个标准策略是什么？

## A zh
客户端的 TCP 接收窗口填满，服务器的内核发送缓冲填满，然后**每连接应用队列无界增长** — 少数缓慢消费者可以耗尽服务器内存。

- **丢弃**最旧/最新 — 当消息独立时很好。
- **合并** — 仅保留每个 key 的最新值（ticker、presence、cursor）：当消息是快照而不是增量时理想。
- **断开连接**超过队列阈值 — 客户端重新连接并从真实源重新同步。

按语义选择：增量需要可靠传递或在间隙上重新同步；快照始终可以合并。
