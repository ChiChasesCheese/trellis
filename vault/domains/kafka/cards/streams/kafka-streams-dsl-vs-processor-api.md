---
id: kafka-streams-dsl-vs-processor-api
node: streams.streams-api
type: qa
step: 3
source: kafka-2e
---
## Q
Kafka 提供了两套构建流式处理逻辑的 API：底层的 Processor API 和高级的 Streams DSL（domain specific language，领域特定语言）。写字数统计、股票统计这类应用时，为什么通常优先选用 Streams DSL 而不是 Processor API？

## A
Streams DSL 让开发者通过给一个 KStream/KTable 声明式地串联一连串转换（比如 flatMapValues、filter、groupByKey、aggregate）来定义处理拓扑，绝大多数常见的过滤、聚合、连接需求都能用几行链式调用表达清楚，简单直观、上手成本低。Processor API 是更底层的接口，需要开发者自己实现每个处理节点的具体逻辑，灵活性更高（可以做 DSL 表达不了的自定义处理），但相应地写起来更繁琐。所以只有在 DSL 提供的内置转换满足不了业务需求时，才需要退到 Processor API 自己实现转换逻辑。
