---
id: hi-pt-tt-realtime-auction-bidding-10-why-not-redis-lock
node: tt.sd.tt-realtime-auction-bidding.points
type: qa
step: 10
---
## Q
**实时竞价拍卖 · 为什么不全放 Redis、不用全局锁**｜出自：实时竞价拍卖 › 取舍与追问

追问：为什么不把拍卖全放 Redis？为什么不用全局分布式锁？

## A
**Redis。** 出价是金钱承诺，价格倒退或丢出价比慢几毫秒严重得多；Redis 适合读缓存和订阅状态，不适合当唯一账本。
**全局锁。** 锁服务成为瓶颈和单点，租约过期还可能出现两个持有者。按拍卖路由加数据库条件写入，把争用缩到一场拍卖内。
**体验。** 出价者同步拿明确结果，观众允许 200 毫秒滞后。
