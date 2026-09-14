---
id: kafka-reliability-follower-isr-three-conditions
node: reliability.guarantees
type: qa
source: kafka-2e
---
## Q
一个跟随者副本（follower replica）要被算作同步副本、留在 ISR（in-sync replicas，同步副本集合）里，必须同时满足哪三个条件？只要有一个不满足会怎样？

## A
三个条件：1）与 ZooKeeper 保持活跃会话，也就是最近 6 秒（可配置）内向 ZooKeeper 发送过心跳；2）最近 10 秒（可配置）内从首领那里复制过消息；3）不仅复制过消息，而且是复制到了**最新**的消息——单纯「还在复制，但一直追不上最新进度」超过 10 秒同样不合格。只要有一条不满足（比如与 ZooKeeper 断连、停止复制，或复制滞后超过 10 秒），这个副本就会被判定为不同步，移出 ISR；之后只要重新满足条件（比如恢复与 ZooKeeper 的连接并追上最新消息）就能重新加入 ISR。
