---
id: kafka-streams-topologytestdriver-limitation
node: streams.streams-architecture
type: qa
step: 3
source: kafka-2e
---
## Q
TopologyTestDriver 是测试 Kafka Streams 应用拓扑的推荐工具，它让测试代码可以像普通单元测试一样：把数据写入模拟输入主题、运行拓扑、再从模拟输出主题读取结果做断言。但用它测试有一类问题检测不出来，是什么？

## A
TopologyTestDriver 没有模拟 Streams 内部的缓存行为（一种用于减少不必要中间结果写入下游的优化机制），所以任何只有在真实缓存生效时才会暴露出来的问题，用这个工具是测不出来的。因此它适合作为快速、轻量、易调试的单元测试手段，但不能完全替代需要跑真实 broker 的集成测试或端到端测试。
