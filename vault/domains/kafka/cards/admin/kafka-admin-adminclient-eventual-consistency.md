---
id: kafka-admin-adminclient-eventual-consistency
node: admin.topic-ops
type: qa
step: 1
source: kafka-2e
---
## Q
调用 AdminClient.createTopics 创建一个新主题，等它返回的 Future 完成（表示操作成功）后立刻调用 listTopics()，为什么返回的主题列表里有时还看不到这个刚创建的主题？

## A
Kafka 的管理操作（创建、删除、修改）都是发给集群控制器（controller，负责维护集群元数据的特殊 broker）处理的，AdminClient 的 Future 在**控制器**完成状态更新后就算完成，但控制器把这次变更同步给其他 broker 是一个异步过程。这时可能还有 broker 没收到最新元数据，而 listTopics 这类读操作恰好可能被这样的 broker 处理，于是看不到刚创建的主题。这种「最终所有 broker 都会知道，但不保证是在什么时刻」的行为叫作最终一致性（eventual consistency）：用 AdminClient 时不能假设一个写操作完成后，紧随其后的读请求就一定能立刻反映这次变更。
