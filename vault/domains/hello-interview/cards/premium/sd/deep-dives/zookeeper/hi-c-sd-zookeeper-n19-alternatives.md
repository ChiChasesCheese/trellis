---
id: hi-c-sd-zookeeper-n19-alternatives
node: sd.deep-dives.zookeeper.notes
type: qa
step: 18
---
## Q
**ZooKeeper · 替代方案：etcd、Consul、云服务**｜摘要 · 必会

ZooKeeper 之外有哪些协调方案，各适合什么？

## A
- **etcd：** 云原生环境流行，驱动 Kubernetes。强一致分布式键值存储，提供现代的 HTTP/JSON 和 gRPC 接口，为小数据集、高读量优化，适合配置管理和服务发现。
- **Consul（HashiCorp）：** 服务发现、健康检查加键值存储；特色是网络基础设施自动化，能按服务变化动态配置负载均衡器和防火墙，比 ZooKeeper 更全面。
- **云厂商方案：** AWS Parameter Store、Azure App Configuration 等，托管、几乎不用配置运维，面试里值得提。
- **更高层的内置服务：** AWS ECS 的集中控制面、CloudMap 做服务发现、MSK 托管整套 Kafka（旧版本连 ZooKeeper 一起托管，新版本用 KRaft）。
- **用法：** 能用平台自带的就不要自己维护一个共识集群。
