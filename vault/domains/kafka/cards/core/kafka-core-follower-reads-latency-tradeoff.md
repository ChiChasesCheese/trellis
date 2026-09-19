---
id: kafka-core-follower-reads-latency-tradeoff
node: core.replication-isr
type: qa
step: 5
source: kafka-2e
---
## Q
KIP-392 引入了「从跟随者副本读取数据」的特性，让消费者可以从地理上更近的副本读取而不总是从首领读。这样做要付出什么代价？

## A
为了保证从跟随者读到的消息也是已提交（committed）的，首领要把当前的高水位标记（最近一次成功提交的偏移量）随数据一起发给跟随者，跟随者据此才能对外暴露已提交的消息，这个传递过程带来额外延迟。所以从跟随者副本读到数据会比直接从首领副本读取更晚出现；如果业务对消费延迟敏感，应继续从首领读取，只有当降低网络成本（如跨机房流量）比延迟更重要时，才配置消费者的 client.rack 和 broker 的 replica.selector.class 启用按机架就近读取。
