---
id: kafka-eos-idempotent-pid-sequence-dedup
node: eos.idempotent-producer
type: qa
source: kafka-2e
---
## Q
开启幂等生产者（`enable.idempotence=true`）之后，broker 是靠什么信息识别出「这条消息其实是刚才那条消息的重发」，从而拒绝写入重复数据的？

## A
每条消息都会带上生产者在启动时申请到的**生产者 ID（PID）**和一个按序递增的**序列号**；PID + 序列号再加上目标主题和分区，就能唯一标识一条消息。broker 会为每个分区记住来自每个生产者的最近 5 条消息的序列号（生产者要把 `max.in.flight.requests`——同时未确认的在途请求数——设为 5 或更小才能让这个跟踪机制生效，5 也是默认值）。如果 broker 收到一条它已经处理过的（PID+序列号组合重复的）消息，就会拒绝写入并返回错误，但生产者只会把它记录到指标里，不会抛异常或报警——因为对生产者来说，这本来就是它自己在重试，这次重试「被去重」是预期内的正常结果。
