---
id: kafka-producer-compression-snappy-vs-gzip
node: producer.batching-throughput
type: qa
source: kafka-2e
---
## Q
`compression.type` 可选 snappy、gzip、lz4、zstd 等压缩算法。在「CPU 开销」和「压缩率」上，snappy 和 gzip 分别适合什么场景？

## A
snappy 占用较少的 CPU 时间，同时能提供不错的性能和压缩比，适合同时关心性能和网络带宽的场景；gzip 通常占用更多 CPU 时间，但压缩比更高，适合网络带宽比较紧张、更需要省流量的场景。压缩能降低网络传输和存储的开销，而这往往是发送消息时的瓶颈所在，默认情况下 Kafka 不压缩消息。
