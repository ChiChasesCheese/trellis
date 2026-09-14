---
id: kafka-eos-idempotent-out-of-order-seq-error
node: eos.idempotent-producer
type: qa
source: kafka-2e
---
## Q
启用幂等生产者后，如果 broker 期望收到序列号 3，却直接收到了序列号 27，broker 会返回什么错误？这个错误说明了什么潜在问题，值得怎么排查？

## A
broker 会返回「乱序（out of order）」错误；如果没有开启事务，这个错误可能被生产者忽略，生产者仍会继续正常运行。但这个现象本身通常意味着**序列号 3 到 26 之间的消息发生了丢失**——broker 既然从 2 跳到了 27，中间那些理应发生的写入并没有真正落到这个 broker 上。看到这类日志应当去检查生产者和主题的可靠性相关配置是否到位（比如 `acks`），并核查是否发生过不彻底的首领选举（unclean leader election）导致部分已确认的消息在切换首领后凭空消失。
