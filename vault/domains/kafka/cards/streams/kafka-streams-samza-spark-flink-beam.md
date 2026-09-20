---
id: kafka-streams-samza-spark-flink-beam
node: streams.choosing-framework
type: qa
step: 5
source: kafka-2e
---
## Q
Samza、Spark、Flink、Beam 都可以用于流式处理，但设计定位差别很大：如果需要极低延迟的逐事件处理，如果更看重容错和广泛的社区生态、可以接受微批次带来的延迟，如果想用一套代码同时兼顾流处理和批处理，分别应该倾向选哪一个？

## A
需要极低延迟的逐事件处理，应该倾向 **Flink**——它专门面向流式处理设计，延迟非常低，除了 Yarn 还能运行在 Mesos、Kubernetes 或独立集群上，并且高级 API 支持 Python 和 R。更看重容错能力和广泛社区支持、能接受微批次延迟的，倾向 **Spark**——它本质是面向批处理的项目，通过把数据流切成一个个微批次来处理，延迟比逐事件模型更高，但可以通过重新处理某个批次来实现容错，还能方便地实现 Lambda 架构。想用同一套编程模型统一表达批处理和流处理逻辑、并能把处理逻辑运行在不同底层引擎上的，应该用 **Beam**——它本身不是一个执行引擎，而是一种统一编程模型，可以把 Samza、Spark、Flink 当作底层的运行器（runner）来执行同一份管道代码。**Samza** 则是专为 Kafka 设计、和 Streams 同一批人开发、共享很多概念的框架，但它运行在 Yarn 上并提供了一整套独立的应用运行框架，不像 Streams 只是一个可以直接嵌入普通 Java 应用的库。
