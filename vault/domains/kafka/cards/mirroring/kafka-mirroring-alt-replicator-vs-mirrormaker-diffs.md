---
id: kafka-mirroring-alt-replicator-vs-mirrormaker-diffs
node: mirroring.alternatives
type: qa
step: 3
source: kafka-2e
---
## Q
Confluent Replicator 和 MirrorMaker 都基于 Connect 框架构建，功能上有几处明显差异：在 ACL（访问控制列表）迁移、跨语言客户端的偏移量迁移，以及「本地/远程主题」概念上，Replicator 分别是怎么处理的？

## A
在 ACL 迁移上，Replicator 完全**不支持**迁移 ACL，这一点和支持迁移 ACL 的 MirrorMaker 不同。在偏移量迁移上，Replicator 只支持 **Java 客户端**（通过时间戳拦截器实现），覆盖面比 MirrorMaker 更窄。在主题命名模型上，Replicator **没有**「本地主题」和「远程主题」这种区分（也就没有 MirrorMaker 那种给远程主题自动加集群前缀的机制），但它换了一种方式支持把多个源的同名主题**聚合**到一起；为了同样避免循环复制，Replicator 依靠消息头里记录的「来源」信息来识别并阻止一条消息被重复镜像回它的源头，而不是靠主题命名前缀。
