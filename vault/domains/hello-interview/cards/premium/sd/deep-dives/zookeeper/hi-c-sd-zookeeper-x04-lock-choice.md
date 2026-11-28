---
id: hi-c-sd-zookeeper-x04-lock-choice
node: sd.deep-dives.zookeeper.exam
type: qa
step: 4
---
## Q
**ZooKeeper · 锁用 ZooKeeper 还是 Redis**｜考点 · 必会

(a) 电商秒杀对库存加锁，每秒数千次、持锁几毫秒；(b) 夜间批处理任务要独占某个资源数小时；(c) 转账时对账户加锁，错误代价极高。各选什么？

## A
- **(a) Redis 锁或数据库行锁：** 高频、短持有，ZooKeeper 的写要经领导者多数确认，吞吐不够。
- **(b) ZooKeeper：** 持锁很久，临时节点在持有者崩溃时自动释放，不需要自己管理超时续约和心跳。
- **(c) 数据库事务或 ZooKeeper：** 正确性优先。用数据库事务直接保证最稳妥；需要跨多个系统协调时再用 ZooKeeper，并配合防护令牌。
- **选择依据：** 加锁频率、持锁时长、出错代价。
