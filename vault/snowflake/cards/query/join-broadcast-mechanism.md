---
id: join-broadcast-mechanism
node: query.join-strategies-broadcast-shuffle
type: qa
tags: [grown]
---
## Q
在多节点虚拟仓库（virtual warehouse）上把一张 10 亿行的事实表与一张 1 万行的维表做等值连接，广播连接（broadcast join）怎样执行？为什么适合这种情况？

## A
把小的维表完整复制（广播）到每个工作节点，各节点用它构建哈希表；大的事实表不移动，每个节点只用本地分到的那部分事实表数据去探测哈希表。网络上只传输一份小表 × 节点数的数据，大表完全不需要重新分布，因此在一侧很小时代价最低。
