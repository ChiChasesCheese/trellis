---
id: join-shuffle-mechanism
node: query.join-strategies-broadcast-shuffle
type: qa
tags: [grown]
---
## Q
两张都有数亿行的表做等值连接时，为什么通常不能用广播连接，而要用洗牌连接（shuffle / hash-repartition join）？它的代价在哪里？

## A
广播要把一侧完整复制到每个节点，一侧很大时既占满每个节点的内存又产生巨量网络传输。洗牌连接则按连接键的哈希值把两侧数据都重新分布到各节点，保证键相同的行落到同一节点，再在每个节点上各自做本地哈希连接，每个节点只需容纳一部分数据。代价是两侧都要经过网络重分布，数据移动量与两表总大小成正比。
