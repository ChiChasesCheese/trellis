---
id: kafka-internals-fetch-zero-copy
node: internals.request-handling
type: qa
source: kafka-2e
---
## Q
Kafka 的 broker 在处理获取请求（fetch request，消费者/跟随者副本用来拉取消息的请求）时，为什么用「零复制（zero-copy）」技术发送消息，它省掉了什么？

## A
零复制指 broker 把消息直接从磁盘文件（实际常常是 Linux 文件系统缓存）发送到网络通道，中间不经过应用层的任何缓冲区，也就不需要先把数据拷贝进 broker 进程的内存再拷贝出去。相比很多数据库那种「先读进本地缓存、处理后再发送」的做法，零复制省掉了字节复制的开销和内存缓冲区的管理成本，因此获取请求的吞吐和延迟表现更好。
