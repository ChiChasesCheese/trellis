---
id: kafka-producer-acks-speed-vs-durability-tradeoff
node: producer.acks-durability
type: qa
step: 1
source: kafka-2e
---
## Q
从 acks=0 到 acks=1 再到 acks=all，生产者发送消息的「速度」和「可靠性」之间存在什么规律？

## A
acks 的值设得越小，生产者不用等待越多的确认，发送速度（生产者视角的延迟）就越快，但可靠性越低：acks=0 完全不等待、可能悄悄丢消息，acks=1 只等首领、首领崩溃时仍可能丢消息，acks=all 等所有同步副本确认、最安全但因为要等更多网络往返而生产者延迟最高。也就是说这三档配置是用可靠性换取生产者延迟的权衡。
