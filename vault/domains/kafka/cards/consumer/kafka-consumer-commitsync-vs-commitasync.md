---
id: kafka-consumer-commitsync-vs-commitasync
node: consumer.offset-commit
type: qa
step: 4
source: kafka-2e
---
## Q
`commitSync()` 和 `commitAsync()` 都能手动提交偏移量，二者最主要的区别是什么？为什么 `commitAsync()` 遇到提交失败时不会像 `commitSync()` 那样自动重试？

## A
`commitSync()` 会阻塞，直到 broker 确认提交成功或者抛出异常，如果失败就持续重试，可靠但限制吞吐量；`commitAsync()` 发出提交请求后立刻返回、不等待响应，吞吐量更高，但失败时默认不重试。不重试的原因是：如果一次异步提交（比如偏移量2000）因为网络问题延迟到达，而在这期间又有一次更晚的提交（偏移量3000）先成功了，这时候如果再重试那个旧的2000，反而可能在3000之后把偏移量「压低」回2000，一旦此时发生再均衡，就会导致原本已经处理过的消息被重复处理。
