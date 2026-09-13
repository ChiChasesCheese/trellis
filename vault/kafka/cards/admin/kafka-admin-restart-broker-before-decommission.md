---
id: kafka-admin-restart-broker-before-decommission
node: admin.partition-reassignment
type: qa
source: kafka-2e
---
## Q
计划把一个 broker 的所有分区都搬走、然后把它从集群里移除时，有一个技巧：先重启这个即将被移除的 broker，再执行分区重分配，为什么这样能显著提升重分配的效率？操作时要注意什么？

## A
broker 重启（关闭）的过程会让它上面所有的分区首领自动转移给其他 broker；如果不这么做，重分配开始时这个 broker 往往还持有大量分区的首领，首领所在 broker 要承担该分区全部的读写和向其它副本复制数据的流量，会成为整个重分配过程的瓶颈。提前把首领转移出去后，原本集中在一台机器上的复制流量就被分摊到了其他多个 broker 上，显著减少对集群的整体影响。需要注意的是，如果集群启用了自动首领重分配，这个 broker 重启回来后可能会重新拿回部分首领权，所以操作期间最好临时禁用自动首领重分配。
