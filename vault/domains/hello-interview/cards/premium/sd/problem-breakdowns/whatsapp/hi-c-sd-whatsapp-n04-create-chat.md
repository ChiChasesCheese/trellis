---
id: hi-c-sd-whatsapp-n04-create-chat
node: sd.problem-breakdowns.whatsapp.notes
type: qa
step: 4
---
## Q
**WhatsApp 即时通讯 · 高层设计：建群与数据表**｜摘要 · 必会

建群在系统里怎么实现？为什么负载均衡用 L4，群成员表怎么设计才能两个方向都能查？

## A
- **流程：** 客户端连上服务并发 `createChat`；服务在库里写一条 Chat 记录和每个成员各一条 ChatParticipant 记录；返回 chatId。数据库选 DynamoDB，因为键值访问快、容易扩展。
- **写入细节：** 小群可用一个 DynamoDB 事务写完（事务最多 100 条），群接近 100 人时要分批写。
- **L4 为什么够：** 连接是 WebSocket，不需要按路径或请求头把流量分给不同服务，也不需要把同一连接里的 HTTP 请求拆到不同服务器——这些是 L7 的强项，这里用不上。L4 只转发 TCP 连接，开销更小、性能更高。现代 L7 也支持 WebSocket，所以说"能用，但没必要"。
- **Chat 表：** 只按 chatId 查，主键就是 chatId。
- **ChatParticipant 表要两个方向：**
  - 查一个群的所有成员：复合主键，chatId 为分区键、participantId 为排序键，对 chatId 做一次 Query；
  - 查一个用户的所有群：建全局二级索引（GSI），participantId 为分区键、chatId 为排序键，DynamoDB 自动与基表同步。
