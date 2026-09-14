---
id: kafka-practice-azure-managed-vs-ephemeral-disk
node: practice.cloud-deployment
type: qa
source: kafka-2e
---
## Q
在 Azure 上自己搭建 Kafka 集群时，为什么强烈建议给 broker 使用 Azure 托管磁盘（managed disk），而不是虚拟机自带的临时磁盘（ephemeral disk）？

## A
Azure 里虚拟机和磁盘是分开管理的，临时磁盘的生命周期和这台虚拟机实例绑定在一起——一旦这台虚拟机因为底层维护、故障迁移等原因被移动到另一台物理主机，挂载在原实例上的临时磁盘数据就会丢失，这意味着这个 broker 保存的所有消息数据都可能凭空消失。使用 Azure 托管磁盘则可以独立于具体虚拟机实例持久化保存，即使虚拟机被迁移，数据依然完好，能避免这种因为底层运维操作而导致 broker 数据丢失的风险。
