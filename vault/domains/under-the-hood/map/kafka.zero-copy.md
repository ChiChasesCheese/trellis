%% trellis:begin %%
# 页缓存、零拷贝与批量
*Kafka*

Kafka 不自己做缓存而用操作系统页缓存；消费时 sendfile 直接从页缓存送到网卡；批量 + 压缩把小消息变成大块顺序 I/O。

**Core** — part of the first pass through this subject.

## Cards (3)
1. [[uth-kafka-zero-copy-1-page-cache]]
2. [[uth-kafka-zero-copy-2-sendfile]]
3. [[uth-kafka-zero-copy-3-batch-compress]]
%% trellis:end %%

## Notes
