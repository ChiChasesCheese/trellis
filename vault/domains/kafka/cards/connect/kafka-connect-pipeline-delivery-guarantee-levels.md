---
id: kafka-connect-pipeline-delivery-guarantee-levels
node: connect.pipeline-design
type: qa
source: kafka-2e
---
## Q
数据管道对「传递保证」的要求通常分为哪两个级别？Kafka 本身天然支持哪一级，要做到更高一级的保证，还需要依赖什么条件？

## A
两个级别：**至少一次传递**（at-least-once，源系统的每个事件都必须到达目的地，但重试可能导致同一事件被传递不止一次）和**精确一次传递**（exactly-once，每个事件必须到达且不能丢也不能重复）。Kafka 本身天然支持至少一次传递；要实现精确一次传递，需要 Kafka 的事务机制，再配合目标端点自身支持事务模型或具备唯一键（用来去重/幂等写入）这类能力——Connect API 提供了处理偏移量的接口，让开发者可以据此构建出端到端支持精确一次传递的数据管道，很多开源连接器（connector）也已经原生支持这种保证。
