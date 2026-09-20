---
id: kafka-practice-strimzi-operator-not-managed-service
node: practice.kubernetes-strimzi
type: qa
step: 1
source: kafka-2e
---
## Q
在 Kubernetes 上想要运行自己的 Kafka 集群（而不是用某个云厂商的全托管 Kafka 服务）时，Strimzi 扮演的是什么角色？它和一个「全托管 Kafka 平台」的根本区别是什么？

## A
Strimzi 提供的是一个 Kubernetes Operator（一种通过声明式的 Kubernetes 自定义资源来自动化管理某个应用生命周期的模式）：用户只需要用 Kubernetes 资源描述期望的 Kafka 集群状态（比如多少个 broker、用什么配置），Strimzi 就会在公有云或私有云的 Kubernetes 环境里自动完成 Kafka 的启动、运行等操作，大大简化了在 Kubernetes 上部署和运维 Kafka 的过程。但它本身**不提供托管服务**——用户仍然要在自己的 Kubernetes 集群里承担运行这些 Pod 所需的计算、存储资源，以及底层 Kubernetes 集群本身的运维责任，这一点和把整个 Kafka 集群完全交给云厂商托管的服务有本质区别：Strimzi 简化的是「怎么在你自己的 Kubernetes 里跑起来」，而不是「帮你把 Kafka 整个管起来」。
