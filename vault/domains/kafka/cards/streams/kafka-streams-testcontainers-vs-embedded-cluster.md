---
id: kafka-streams-testcontainers-vs-embedded-cluster
node: streams.streams-architecture
type: qa
source: kafka-2e
---
## Q
对 Kafka Streams 应用做集成测试，EmbeddedKafkaCluster（broker 和测试代码跑在同一个 JVM 里）和 Testcontainers（broker 跑在 Docker 容器里）是两个常见选择，为什么优先推荐 Testcontainers？

## A
EmbeddedKafkaCluster 把 broker 和被测代码放进同一个 JVM 进程运行，测试环境和真实生产环境的隔离程度较低，测试代码的类加载、依赖冲突等问题可能干扰到内嵌 broker，也更难完全模拟真实网络行为。Testcontainers 借助 Docker，把 Kafka、它依赖的组件以及测试所需的其他资源都跑在独立容器里，与被测应用程序进程完全隔离，测试环境更接近真实部署，也不会因为共享 JVM 而互相污染，因此更值得优先使用。
