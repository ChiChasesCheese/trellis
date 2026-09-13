---
id: kafka-eos-transactions-zombie-fencing-epoch
node: eos.transactions
type: qa
source: kafka-2e
---
## Q
使用事务性生产者时，配置的 `transactional.id`（事务 ID，跨重启保持不变）是怎么配合 epoch（每次初始化递增的代数）来阻止「僵尸」实例（已经被判定死亡、但自己不知道、还在继续写数据的旧实例）写入重复结果的？

## A
事务性生产者每次调用 `initTransactions()` 初始化时，broker 都会把这个 `transactional.id` 对应的 epoch 加一。之后凡是带着**同一个** `transactional.id` 但 epoch 比当前值小的发送、提交、中止请求，都会被 broker 拒绝并返回 `ProducerFencedException`（生产者被隔离异常），旧实例因此无法再写入任何数据，只能被迫关闭。也就是说，只要新实例用相同的 `transactional.id` 重新初始化了一次，它自动获得更高的 epoch，旧的「僵尸」实例发出的任何请求都会因为 epoch 过期被挡下来，从根本上避免了僵尸重复写入的问题。
