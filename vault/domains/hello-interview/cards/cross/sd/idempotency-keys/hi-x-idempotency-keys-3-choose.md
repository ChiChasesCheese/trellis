---
id: hi-x-idempotency-keys-3-choose
node: sd.cross.idempotency-keys
type: qa
step: 3
---
## Q
**幂等键与只生效一次**｜跨题模式 · 怎么选

拿到一个新的「会被重复请求」的设计题，怎样判断幂等要做到哪一层、用哪种形态？给出判断信号，每个分支配一个例子。

## A
按下面几个信号依次判断：

| 信号 | 该怎么做 | 例子 |
|---|---|---|
| 重复会造成资金损失或不可逆动作 | 唯一约束占键，业务和结果同事务，保存「进行中」状态和请求指纹，业务拒绝也记住 | [[tt-idempotent-transfer\|幂等转账服务]] |
| 副作用发生在外部系统 | 键要一路传下去（给 PSP、余额服务、书商、网络），并确认对方支持幂等和查询；超时当 UNKNOWN，不当失败 | [[donations-website-charities\|设计限时捐款网站]]、[[book-seller-platform\|图书比价代购平台（Book Seller Platform）]] |
| 重复来自内部重试或故障转移，没有用户请求 | 每次执行有稳定标识，CAS 防双发，租约加围栏令牌，任务本身要幂等 | [[job-scheduler-cron-history\|分布式任务调度器（含 cron 与一年执行历史）]] |
| 下游是至少一次的事件流 | 消费者也按事件 ID 去重，入口和出口各有一个去重键 | [[tt-live-gift-coin-settlement\|直播虚拟礼物：金币记账与主播结算]] |
| 同时要求唯一的先后顺序 | 幂等加单一拥有者、世代号或序号 | [[tt-realtime-auction-bidding\|实时竞价拍卖]]、[[messenger-chat-system\|设计聊天/即时通讯系统（WhatsApp / Messenger）]] |
| 重复只是多显示一条，代价低 | 客户端 ID 加会话序号即可，不必保存完整响应 | [[messenger-chat-system\|设计聊天/即时通讯系统（WhatsApp / Messenger）]] |

口诀：先问「重复一次的代价是什么」，再问「副作用在谁手里」。
