---
id: kafka-connect-smt-vs-streams-boundary
node: connect.smt
type: qa
source: kafka-2e
---
## Q
Kafka Connect 里的单一消息转换（SMT，single message transformation）能不能用来实现「把两个主题的数据按某个字段连接（join）起来」或者「按时间窗口聚合统计」这类需求？为什么不行，应该改用什么？

## A
不行。SMT 是**无状态**的：它只能基于当前这一条记录本身的内容做加工（改字段类型、遮蔽字段、过滤、改路由主题等），处理时看不到也不记得其他消息，所以天然做不了需要「记住之前见过的数据」才能完成的操作，比如把两个数据源的记录连接起来，或者把一段时间窗口内的多条消息聚合成一个统计值——这些都需要维护跨消息的状态。这类**有状态**的转换需要用 Kafka Streams（Kafka 提供的有状态流处理框架）来实现。可以把 SMT 理解成「流经 Connect 时顺手做的轻量单条加工」，把 Streams 理解成「需要记忆和关联多条消息的复杂处理」，两者分工不同，不能互相替代。
