---
id: hi-ov-top-k-2-options
node: sd.problem-breakdowns.top-k
type: qa
step: 2
tags: [通览]
---
## Q
**YouTube 热门 Top K · 高层设计**｜通览

YouTube 热门 Top K 的高层设计怎么搭？每个功能需求走哪条路径？

## A
**组件。** 按视频 ID 分区的 Kafka、消费者、Postgres、负载均衡后的 Top K 服务。

**每条路径。**
- **全时间前 K：** 消费者读播放事件，把 Postgres 里该视频的计数加一；查询在 views 列的索引上取前 k 行，近似 O(k)。
- **窗口前 K：** 表里加小时整点时间戳，每个视频每小时一行；查询要跨小时求和再排序，要扫描大量行，这是留给深挖的瓶颈。

**存储。** 计数放 Postgres，views 列建索引让排序直接可读；代价是每次写都要更新索引，所有写入压在一个实例上，这些先说出来，后面再解决。
