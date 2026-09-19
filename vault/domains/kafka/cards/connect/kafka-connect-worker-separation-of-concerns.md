---
id: kafka-connect-worker-separation-of-concerns
node: connect.connect-basics
type: qa
step: 4
source: kafka-2e
---
## Q
Connect 的 worker（承载连接器和任务运行的节点，多个 worker 组成一个 worker 集群）具体负责哪些事情？为什么说「连接器和任务负责搬数据、worker 负责搬数据之外的一切」是 Connect API 相对普通客户端 API 的最大优势？

## A
worker 负责处理创建/管理连接器的 REST 请求、把连接器配置持久化到内部 Kafka 主题、启动连接器和任务并给任务分发配置、自动把偏移量提交到内部主题，以及在任务抛异常时重试；如果某个 worker 崩溃，集群里其他 worker 会通过消费者协议的心跳机制感知到，并把它上面的连接器和任务重新分配出去，新 worker 加入时也会自动帮忙分摊负载。这种「连接器/任务只管数据怎么搬，worker 统一管配置管理、可靠性、高可用、伸缩性和负载均衡」的关注点分离，意味着任何一个连接器插件的开发者都不需要重新实现这些复杂的基础设施能力——而如果是自己写的普通客户端小程序，这些能力都得自己从零构建。
