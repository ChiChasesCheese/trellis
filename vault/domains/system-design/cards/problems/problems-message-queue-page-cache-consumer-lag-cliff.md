---
id: problems-message-queue-page-cache-consumer-lag-cliff
node: problems.foundations.message-queue
type: qa
step: 4
tags: [grown]
---
## Q
In a Kafka-class message queue relying on the OS page cache (not an in-process cache) to serve reads, why does a consumer's lag falling behind roughly 15-16 minutes (in a design where 50GB of page cache buffers about 52.9MB/s of per-broker peak write traffic) create a problem for OTHER producers and consumers on the cluster, not just for that one lagging consumer?

## A
As long as a consumer's read position stays within the recent window still held in page cache (about 945 seconds here), its fetches are served from memory via zero-copy and cost the broker almost nothing extra. Once a consumer falls further behind than that window, its reads start missing the page cache and hitting the disk directly -- and because that disk is the same device the partition leader is using for its own sequential append writes, the lagging consumer's random-ish reads now compete for the same disk I/O bandwidth as the write path. The result is that one consumer falling behind can measurably slow down write latency for every producer on that broker, not just degrade the lagging consumer's own read latency.

## Q zh
在一个依赖操作系统 page cache（而非进程内缓存）来服务读请求的 Kafka 一类消息队列里，如果消费者滞后（lag）超过大约 15-16 分钟（本设计里 50GB page cache 大约能缓冲每台 broker 峰值写入流量 52.9MB/s 所对应的时长），为什么这不仅会让这一个滞后的消费者变慢，还会给集群上其他生产者和消费者造成问题？

## A zh
只要消费者的读取位置还落在 page cache 覆盖的最近窗口内（此处约 945 秒），它的拉取请求走内存、通过零拷贝服务，几乎不给 broker 带来额外开销。一旦消费者滞后超过这个窗口，它的读请求就开始未命中 page cache、直接打到磁盘——而这块磁盘正是分区 leader 用来做自己顺序追加写入的同一个设备，滞后消费者这种偏随机的读请求由此和写路径争抢同一份磁盘 I/O 带宽。结果是一个滞后的消费者可以显著拖慢这台 broker 上所有生产者的写入延迟，而不只是让这个滞后消费者自己的读延迟变差。
