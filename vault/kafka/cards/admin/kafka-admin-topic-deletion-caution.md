---
id: kafka-admin-topic-deletion-caution
node: admin.topic-ops
type: qa
source: kafka-2e
---
## Q
用 `kafka-topics.sh --delete` 删除一个主题，broker 端必须满足什么前置条件才会真的执行删除？为什么在大型集群里不建议连续、一次性删除很多个主题？

## A
broker 的配置参数 `delete.topic.enable` 必须设置为 true，否则删除请求会被直接忽略，主题不会被删除。即使条件满足，删除也是异步操作：主题先被打上删除标记，控制器（controller，负责维护集群元数据的特殊 broker）要等手头现有任务处理完才能通知各个 broker 让相关元数据失效、并从磁盘删除对应文件，这个过程在大集群里可能需要不短的时间。如果不给前一个删除操作留出足够时间就连续发起多个删除请求，会给控制器造成额外负担，拖慢整体处理速度；另外要牢记删除主题是不可逆操作，没有类似回收站的机制能找回误删的数据。
