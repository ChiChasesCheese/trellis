---
id: kafka-admin-cancel-reassignment-risk
node: admin.partition-reassignment
type: qa
source: kafka-2e
---
## Q
用 kafka-reassign-partitions.sh 的 `--cancel` 选项取消一个正在进行中的分区重分配，会把副本集合恢复成什么状态？为什么这在某些场景下有风险？

## A
取消操作会把分区的副本集合恢复到这次重分配开始之前的状态。但如果这次重分配本来就是为了把副本从一个已经失效或过载的 broker 上移走，取消操作意味着又把这些副本的职责放回给这个本就有问题的 broker，可能让集群回到一个非预期、依旧存在问题的状态；而且取消后恢复出来的副本集合顺序也不能保证和重分配之前完全一致，这会影响到「副本清单中第一个即为首选首领」这类依赖顺序的逻辑。
