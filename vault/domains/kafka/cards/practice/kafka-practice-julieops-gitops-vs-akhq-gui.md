---
id: kafka-practice-julieops-gitops-vs-akhq-gui
node: practice.kubernetes-strimzi
type: qa
source: kafka-2e
---
## Q
JulieOps（之前叫 Kafka 拓扑构建器）和 AKHQ 都可以用来管理 Kafka 的主题和 ACL，但它们背后的管理模型完全不同，分别是什么？

## A
JulieOps 基于 GitOps 模型工作：把主题、模式、ACL 等配置以声明式的方式写在代码/配置文件里（类似「期望状态即代码」），交由 JulieOps 对比当前实际状态和期望状态、自动完成变更，所有配置变更都能像代码一样被版本控制、评审和追溯。AKHQ 则是一个图形界面（GUI）管理和交互工具，管理员通过界面直接查看和修改用户、ACL、主题等配置，是一种更直接、交互式的操作方式，而不是声明式地维护一份配置源。前者更适合需要配置变更可追溯、可评审、走代码流程管理的团队，后者更适合需要快速查看集群状态、手动交互式操作的场景。
