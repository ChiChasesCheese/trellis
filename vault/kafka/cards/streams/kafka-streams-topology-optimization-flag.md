---
id: kafka-streams-topology-optimization-flag
node: streams.streams-architecture
type: qa
source: kafka-2e
---
## Q
用 Streams DSL（领域特定语言）写的每一步转换默认会被独立映射成对应的底层操作，错失了对整体执行计划做优化的机会。要让 Streams 在生成物理拓扑时对整体执行计划进行优化，需要做哪两件事，缺一会怎样？

## A
需要两步同时做到：一是把配置 `StreamsConfig.TOPOLOGY_OPTIMIZATION` 设置为 `StreamsConfig.OPTIMIZE`；二是调用 `StreamsBuilder.build(props)` 时把这份包含该配置的 Properties 对象传进去。如果只调用不带参数的 `build()`，即使配置里已经设置了这个优化开关，也不会生效，因为优化是在「从逻辑拓扑生成物理拓扑」这一步根据传入的配置决定的，没有把配置传给 build 方法，这一步就拿不到开关的值。目前这类优化主要与主题复用有关，建议对开启和不开启两种情况分别测试执行耗时、写入数据量，并核对结果是否一致。
