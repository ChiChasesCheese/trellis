---
id: hi-x-atomic-conditional-update-3-choose
node: sd.cross.atomic-conditional-update
type: qa
step: 3
---
## Q
**原子条件更新与防超卖**｜跨题模式 · 怎么选

遇到“有限资源被并发抢占”的题，怎么决定原子手段？请按资源形态和请求规模分情况说明，并各举一例。

## A
| 判断信号 | 手段 | 例子 |
|---|---|---|
| 单个热点计数器，冲突很多 | 一条条件更新，不用乐观版本号（开售瞬间冲突率极高，重试浪费）；悲观锁只留给要同时锁多个资源的场景，并固定加锁顺序 | [[event-ticket-booking\|活动票务预订后端（防超卖的 REST 服务）]] |
| 一次要占多行，必须全成或全败 | 同一事务里逐行条件扣减，影响行数必须等于行数 | [[hotel-booking-system\|酒店预订系统（Expedia 型聚合与自营）]] |
| 请求量远大于库存，单行有约 500 次/秒的上限 | 先准入拦掉大部分，再 Redis 脚本闸门加数据库条件更新；库存很小时准入之后直接数据库 | [[tt-flash-sale-ticketing\|秒杀抢票（排队、限流、防超卖）]]、[[crowdfunding-share-purchase\|设计限时众筹购股系统（用账户余额抢固定数量的公司股份）]] |
| 资源是钱，不允许为负 | 条件里带余额检查，影响行数为 0 就拒绝 | [[tt-wallet-ledger-service\|钱包与复式账本服务（余额、冻结、转账、多币种）]]、[[stock-trading-platform\|设计简化版股票交易平台（券商端，限价单）]] |
| 同一用户并发多笔 | 每用户一把锁，或让条件更新在同一行上天然串行 | [[grocery-subscription-orders\|生鲜订阅转订单服务]] |
| 内存里的类设计 | 一把锁内完成检查并取走，释放要幂等 | [[parking-lot-system\|停车场管理系统]] |
