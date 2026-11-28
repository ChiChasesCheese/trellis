---
id: hi-c-sd-zookeeper-n07-watches
node: sd.deep-dives.zookeeper.notes
type: qa
step: 7
---
## Q
**ZooKeeper · 监视：变更时通知，而不是轮询**｜摘要 · 必会

监视（watch）解决什么问题？它怎样让服务器本地缓存路由信息？

## A
- **问题：** 没有监视，每发一条消息都要查 ZooKeeper 找收件人，延迟高，ZooKeeper 成为瓶颈。
- **用法：** 服务器启动时对 `/chat-app/users` 设置监视；Bob 换服务器时新服务器更新他的 ZNode；ZooKeeper 回调旧监视者，告诉它该节点变了，监视者再读新值更新本地路由表。
- **取代广播：** 服务器不必彼此连成 n² 的网，都只连 ZooKeeper；变更只通知关心的服务器。
- **故障：** 服务器崩溃，会话结束，临时节点删除，监视者收到通知，可以把对应用户标记为离线。
- **本地缓存模式：** 读自己的缓存，变更时被通知再更新。所以 ZooKeeper 是协调服务，而不是数据库，设计目标是通知变更而不是承担大量读流量。
