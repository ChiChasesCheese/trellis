---
id: kafka-admin-reassignment-throttle
node: admin.partition-reassignment
type: qa
step: 2
source: kafka-2e
---
## Q
用 kafka-reassign-partitions.sh 做分区副本重新分配时，为什么建议搭配 `--throttle` 参数限制复制速率，而不是让重分配尽快跑完？

## A
副本重新分配的本质是把大量数据从旧副本所在的 broker 通过网络复制到新副本所在的 broker，这个过程会占用大量网络带宽和磁盘 I/O，还会打乱操作系统内存缓存页的命中模式，从而挤占集群正常处理生产者/消费者请求所需要的资源，拖慢正常的读写延迟。`--throttle`（以字节/秒为单位）把重分配的复制速率限制在一个安全水位以内，用「重分配总耗时变长」换取「重分配期间不明显影响线上正常流量」，这个参数也可以配合 `--additional` 对一个正在进行中的重分配过程动态调整节流速率。
