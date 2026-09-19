---
id: kafka-mirroring-alt-brooklin-general-purpose
node: mirroring.alternatives
type: qa
step: 2
source: kafka-2e
---
## Q
Brooklin（LinkedIn 开发的镜像方案）和 MirrorMaker、uReplicator 有一个定位上的本质区别：它并不是一个专门为 Kafka 打造的镜像工具。它真正的定位是什么？这个定位让它除了跨集群镜像之外还能做哪些事情？

## A
Brooklin 是一个通用的**分布式数据摄取（data ingestion）服务**，设计目标是在各种异构的数据源和目标系统之间搬运数据，Kafka 只是它支持的众多场景之一。基于这个通用定位，Brooklin 除了可以作为「Kafka 跨集群镜像方案」使用之外，还能充当「数据桥」把不同数据源的数据接入流式处理系统，以及把各类数据存储系统产生的变更数据捕获（CDC，change data capture）事件转化成事件流——三种场景共用同一套底层的分布式数据传输能力。
