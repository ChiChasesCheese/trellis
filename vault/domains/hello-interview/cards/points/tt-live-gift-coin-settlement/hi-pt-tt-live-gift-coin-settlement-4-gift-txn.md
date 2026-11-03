---
id: hi-pt-tt-live-gift-coin-settlement-4-gift-txn
node: tt.sd.tt-live-gift-coin-settlement.points
type: qa
step: 4
---
## Q
**直播礼物金币记账与主播结算 · 送礼的本地事务**｜必会 · 出自：直播礼物金币记账与主播结算 › 整体设计

送礼时礼物服务在钱包分片的一个本地事务里做哪四件事？余额不足怎么处理？

## A
**四件事。** 插入 GiftEvent（`gift_id` 主键冲突说明已处理过，读出第一次的结果）；条件扣币 `UPDATE wallet SET coins = coins - :p WHERE user_id=? AND coins >= :p`；写币流水；写发件箱。
**余额不足。** 影响行数为 0，事务回滚，没有副作用。成功返回最新余额，客户端此刻才确认生效。
**动画。** 房间动画走尽力而为的广播通道，丢了不影响钱。
