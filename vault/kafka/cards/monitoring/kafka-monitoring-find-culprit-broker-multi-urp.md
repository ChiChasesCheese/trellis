---
id: kafka-monitoring-find-culprit-broker-multi-urp
node: monitoring.broker-metrics
type: qa
source: kafka-2e
---
## Q
用 `kafka-topics.sh --describe --under-replicated` 发现有好几个不同主题、不同分区都处于非同步状态，涉及的首领分布在不同 broker 上，此时怎么快速判断问题的根源出在哪一个 broker，而不是整个集群？

## A
把所有非同步分区的 ISR（同步副本集合）和完整副本清单列出来对比，找出哪个 broker 编号**没有出现在任何一条非同步分区的 ISR 里，却出现在所有这些分区的完整副本清单中**——这说明其他 broker 都能正常互相复制，唯独这个 broker 一直无法从别的副本那里把数据复制过来（或者一直不能被别的副本复制），它才是真正的问题根源，应该优先排查这台 broker 的硬件、磁盘或网络状况；如果找不到这样一个「共同嫌疑」的 broker，问题更可能出在集群整体层面（比如负载不均衡或资源过度消耗），而不是某一台机器。
