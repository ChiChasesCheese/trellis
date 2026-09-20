---
id: kafka-reliability-retryable-vs-nonretryable-errors
node: reliability.producer-reliable
type: qa
step: 1
source: kafka-2e
---
## Q
生产者收到 broker 返回的错误后，Kafka 客户端会自动重试某些错误，但另一些错误重试也没用。用 `LEADER_NOT_AVAILABLE`（首领不可用）和 `INVALID_CONFIG`（配置无效）两个错误码举例，说明二者的区别及原因。

## A
`LEADER_NOT_AVAILABLE` 是**可重试错误**：分区首领可能只是暂时缺失（正在选举新首领），过一会儿再发一次，新首领选出来后请求就能成功，所以客户端会自动重试。`INVALID_CONFIG` 是**不可重试错误**：问题出在请求本身的配置有误，不管重试多少次，只要配置不改，结果都会一样失败，重试纯属浪费资源，所以客户端不会对这类错误做自动重试，需要开发者定位并修正配置后才能解决。
