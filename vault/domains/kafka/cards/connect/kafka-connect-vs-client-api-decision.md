---
id: kafka-connect-vs-client-api-decision
node: connect.connect-basics
type: qa
step: 1
source: kafka-2e
---
## Q
什么情况下应该用 Kafka 的生产者/消费者客户端 API 直接对接 Kafka，什么情况下应该改用 Kafka Connect（一个专门用于在 Kafka 和外部数据存储系统之间移动数据的框架）？

## A
如果要连接 Kafka 的应用程序代码是你自己开发、可以随意修改的（比如一个业务服务想主动往 Kafka 写事件或读事件），就直接把生产者/消费者客户端嵌入到这个应用程序里。如果要对接的是一个你没有开发、无法或不想修改其代码的外部数据存储系统（比如 MySQL、ElasticSearch 这类现成系统），就应该用 Connect：只需要给对应的连接器（connector）提供配置文件，不需要写代码去操作这些外部系统的读写细节。
