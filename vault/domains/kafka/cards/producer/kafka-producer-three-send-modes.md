---
id: kafka-producer-three-send-modes
node: producer.client-basics
type: qa
step: 3
source: kafka-2e
---
## Q
Kafka 生产者发送一条消息有三种方式：发送并忘记、同步发送、异步发送。它们在「是否知道发送结果」和「性能」上分别是什么权衡？

## A
「发送并忘记」调用 send() 后不处理返回值，性能最好，但如果发生不可重试的错误或超时，消息会悄悄丢失且应用毫无感知；「同步发送」对 send() 返回的 Future 调用 get() 阻塞等待结果，能确定每条消息是否成功，但发送线程在等待期间什么也做不了，吞吐量差；「异步发送」调用 send() 时传入回调（callback），发送线程不阻塞，Kafka 返回响应时才触发回调处理结果，兼顾了吞吐量和错误可观测性，是推荐的常规做法。
