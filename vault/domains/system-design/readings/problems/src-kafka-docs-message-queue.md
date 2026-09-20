---
nodes: [problems.foundations.message-queue]
url: https://kafka.apache.org/22/design/design/
tags: []
---
# Design | Apache Kafka

值得读：Kafka 官方对存储引擎（顺序 I/O、page cache、zero-copy）、ISR 复制协议、
高水位、log compaction 机制的第一手权威说明，本题解的机制描述均以此为准。比本题解
多讲了配额（quota）机制的实现细节；本题解在此基础上补了针对具体流量规模的分区数、
broker 数、page cache 缓冲时长等算例，这是官方文档本身不给出的部分。

%% trellis:begin %%
## Source
[Open the original ↗](https://kafka.apache.org/22/design/design/)

## Archived copy
![[src-kafka-docs-message-queue-clip]]
%% trellis:end %%
