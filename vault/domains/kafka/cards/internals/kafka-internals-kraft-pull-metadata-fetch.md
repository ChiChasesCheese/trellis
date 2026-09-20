---
id: kafka-internals-kraft-pull-metadata-fetch
node: internals.kraft-mode
type: qa
step: 4
source: kafka-2e
---
## Q
传统架构里，控制器用 `UpdateMetadata` 请求主动把元数据变更**推送**给各个 broker。KRaft 架构把这个方向反过来了，用的是什么新接口，为什么这样对大规模集群更友好？

## A
KRaft 下 broker 改用新的 **MetadataFetchAPI** 主动向主控制器**拉取（pull）**元数据更新，机制类似消费者的获取请求：broker 记录自己已经拉到的元数据偏移量，每次只请求比这个偏移量更新的部分，而不是被动等待推送全部内容。broker 还会把拉到的元数据持久化到本地磁盘上，这样即使集群有数百万个分区，broker 重启后也可以直接从本地磁盘恢复大部分元数据、只按需补齐增量，实现快速启动，减轻了主控制器在大规模场景下集中推送的压力。
