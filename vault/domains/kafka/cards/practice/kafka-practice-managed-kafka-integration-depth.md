---
id: kafka-practice-managed-kafka-integration-depth
node: practice.cloud-deployment
type: qa
source: kafka-2e
---
## Q
选择托管 Kafka 平台时，Amazon MSK、Azure HDInsight 这类「只托管核心 Kafka 集群」的平台，和 Confluent Cloud 这类「整合了模式注册表、REST 代理、客户端库等一整套周边组件」的平台，在使用体验上有什么本质区别？该怎么根据这个区别做选型？

## A
Amazon MSK 和 Azure HDInsight 只负责托管 Kafka 集群本身，模式注册表、REST 代理等周边组件需要用户自己搭建或依赖社区工具（比如 MSK 建议用户自行采用 Cruise Control、Burrow 等社区工具，但平台本身不提供支持服务），集成度较低，但换来的是更贴近原生 Kafka、和其他 AWS/Azure 生态服务集成更顺畅。Confluent Cloud 这类平台把模式管理、REST 接口、客户端库等一整套周边工具都做了原生集成和统一支持，用户不需要自己拼凑和维护这些组件，上手和运维成本更低，但通常会带来额外的平台锁定和许可限制。因此，如果团队本身就熟悉 Kafka 生态、想要更多自由度和更低的平台锁定，选只托管核心集群的方案；如果团队缺乏运维这些周边组件的资源、想要开箱即用的一体化体验，选集成度更高的托管平台。
