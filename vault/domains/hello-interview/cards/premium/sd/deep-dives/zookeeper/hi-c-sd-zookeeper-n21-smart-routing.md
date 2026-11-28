---
id: hi-c-sd-zookeeper-n21-smart-routing
node: sd.deep-dives.zookeeper.notes
type: qa
step: 21
---
## Q
**ZooKeeper · 适用场景：智能路由**｜摘要 · 追问

为什么直播评论、聊天室这类系统可能需要用 ZooKeeper 做路由？

## A
- **问题：** 即使用发布订阅广播消息，也要限制每台服务器订阅的频道数；最好让同一聊天室或同一直播间的用户集中在同一台（或同一组）服务器上，减少跨服务器通信。
- **做法：** 每台服务器在 ZooKeeper 里登记自己的容量和正在处理的房间；网关收到新连接时查询 ZooKeeper，按用户要进的房间决定去哪台服务器。
- **扩容：** 热门房间所有服务器都满了，由 ZooKeeper 协调选一台新服务器加入这个房间的服务集合。
- **适用面：** 这是进阶内容，主要在 Staff 级别，或偏分布式系统方向的 Senior 面试里出现。
