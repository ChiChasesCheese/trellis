---
id: hi-sd-fb-live-comments-7-dispatcher
node: sd.problem-breakdowns.fb-live-comments
type: qa
step: 7
---
## Q
**用调度服务代替发布订阅**｜系统设计 · 题目拆解

直播评论系统里，除了分区 pub/sub，还可以引入调度服务（Dispatcher Service）直接把评论送到相关服务器。请说明它的工作方式、优势与难点，以及 Redis pub/sub 和 Kafka 在这里的取舍。

## A
**做法。** 新评论写入后，评论管理服务问 Dispatcher：“哪些服务器上有人在看这场直播？”Dispatcher 维护动态映射，靠心跳和注册随服务器上下线更新，然后把评论直接转发给这些服务器。多个 Dispatcher 实例放在负载均衡后面，共同读取 ZooKeeper 或 etcd 里的协调数据。

**优势。** 不用管理订阅关系，路由逻辑集中，容易加上按负载路由等规则，实时消息服务器不用改。

**难点。** 病毒式直播让观众突然暴增时，映射必须及时刷新，多个 Dispatcher 的缓存失效要协调，否则会用旧映射。

**消息中间件。** Kafka 容量大、容错好，但不擅长观众频繁切换视频这种动态订阅；Redis pub/sub 延迟低、动态订阅灵活，即发即忘也不要紧，因为评论已落库，漏掉的可以补拉。
