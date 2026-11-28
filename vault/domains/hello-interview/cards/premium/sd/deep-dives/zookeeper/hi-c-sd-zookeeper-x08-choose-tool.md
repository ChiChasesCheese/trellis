---
id: hi-c-sd-zookeeper-x08-choose-tool
node: sd.deep-dives.zookeeper.exam
type: qa
step: 7
---
## Q
**ZooKeeper · 选哪个协调方案**｜考点 · 必会

(a) 团队在 Kubernetes 上做服务发现和配置；(b) 在 AWS 上存动态配置；(c) 运行 HBase 或 ClickHouse 集群；(d) 新部署 Kafka。各选什么？

## A
- **(a) Kubernetes 自带：** 底层就是 etcd，用 Service 做服务发现，用 ConfigMap 放配置，不需要再装 ZooKeeper。
- **(b) 云原生配置服务：** AWS 用 Parameter Store，托管、几乎零运维。
- **(c) ZooKeeper：** 这些系统需要它做复制协调、元数据，是依赖，不是可选项。
- **(d) KRaft：** Kafka 新版本用自带共识替代 ZooKeeper，少部署一套组件。
- **一般原则：** 优先平台自带或系统内置的方案；只有系统本身要求它，或在设计深层基础设施时才主动引入 ZooKeeper。
