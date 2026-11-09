---
id: hi-sd-whatsapp-6-pubsub-durability
node: sd.problem-breakdowns.whatsapp.exam
type: qa
step: 6
---
## Q
**Pub/Sub 至多一次，消息如何不丢**｜系统设计 · 问题拆解

Redis Pub/Sub 只保证至多一次（at most once），转发路径又有额外延迟。写入顺序怎么安排才不丢消息？Redis 单机能承受多大消息量？

## A
**要点。** 先持久化，再尽力推送：
1. **持久：Message 与 Inbox：** 把消息写入 Message 表并创建 Inbox 条目（持久）
2. 向发送方返回成功
3. **实时：Pub/Sub 尽力而为：** 发布到 Pub/Sub 做实时投递（尽力而为）

第 3 步失败也没关系，消息已落库，接收方重连时从 Inbox 同步，或者靠在线客户端的定期检查（轮询、序号缺口检测）补上。

**数字。** Pub/Sub 只做转发、不存储，很轻；单台 Redis 每秒能转发多少条取决于消息大小、订阅者数量和硬件，具体数字要自己压测，设计时先按保守值估实例数。

**取舍。** 代价是多一跳 Redis，增加个位数毫秒延迟，每台聊天服务器还要和 Redis 集群各节点保持连接，但需要的实例数不多，可以接受。
