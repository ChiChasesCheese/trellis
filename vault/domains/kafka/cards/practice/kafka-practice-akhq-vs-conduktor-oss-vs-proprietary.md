---
id: kafka-practice-akhq-vs-conduktor-oss-vs-proprietary
node: practice.kubernetes-strimzi
type: qa
step: 4
source: kafka-2e
---
## Q
AKHQ 和 Conduktor 都是用来查看和操作 Kafka 集群的图形化工具，但在开源属性和支持范围上有明显差异，分别是什么？

## A
AKHQ 是一个开源的 GUI 工具，支持配置管理（包括用户和 ACL 配置），也能对接模式注册表、Kafka Connect 等组件，并提供数据操作能力，可以作为 Kafka 命令行工具的图形化替代品。Conduktor 则不是开源的桌面工具，但同样流行，它支持多个不同的托管平台（包括 Confluent、Aiven 和 Amazon MSK）以及 Connect、kSQL、Streams 等多种组件，也能操作集群数据；它提供了一个可用于操作单个集群的免费许可，超出这个范围则需要付费。选择哪一个，取决于团队是否需要开源、可自行部署和二次开发的方案（AKHQ），还是愿意接受商业授权、换取跨多个托管平台和组件的统一支持体验（Conduktor）。
