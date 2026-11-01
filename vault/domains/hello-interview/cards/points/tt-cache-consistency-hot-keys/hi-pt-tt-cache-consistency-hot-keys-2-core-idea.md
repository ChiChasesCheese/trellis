---
id: hi-pt-tt-cache-consistency-hot-keys-2-core-idea
node: tt.sd.tt-cache-consistency-hot-keys.points
type: qa
step: 2
---
## Q
**缓存一致性与热点 Key · 缓存带来的三件事**｜出自：缓存一致性与热点 Key › 需求

缓存层把一个正确的数据库变成了什么？设计的核心要解决哪三件事？

## A
**要点。** 缓存把"一个正确的数据库"变成"两份会分叉的副本"。
**三件事。** 把不一致窗口压到最小且有兜底；缓存失效时不把数据库压垮；让单个热点 key 的流量落不到某一个节点上。
**分级。** 普通数据允许秒级最终一致，价格、库存、权限等要有更严格路径。
