---
id: kafka-reliability-idempotence-dedupes-retries
node: reliability.producer-reliable
type: qa
step: 3
source: kafka-2e
---
## Q
开启生产者重试后，消息可能因为「响应丢失导致误判失败并重发」而被写入两次。Kafka 提供了什么参数来消除这种因重试造成的重复，而不需要应用自己去做去重？

## A
把 `enable.idempotence` 设为 `true` 即可。开启后，生产者会在每条消息（准确说是每个批次）里附带额外的标识信息，broker 能据此识别出「这其实是刚才那次请求的重发」，从而跳过重复写入，只保留一份。这样，生产者的重试机制既能保证消息不因为网络抖动而丢失，也不会因为重试而产生重复，二者不再是「至少一次」和「精确一次不可兼得」的矛盾。
