---
id: hi-pt-tt-live-gift-coin-settlement-6-exactly-once
node: tt.sd.tt-live-gift-coin-settlement.points
type: qa
step: 6
---
## Q
**直播礼物金币记账与主播结算 · 恰好一次的去重与幂等**｜出自：直播礼物金币记账与主播结算 › 深入 1

充值通知会重复乱序、送礼会重试、事件流至少一次。怎样做到恰好一次？崩溃点怎么收敛？

## A
**机制。** 充值用 `(platform, transaction_id)` 主键同事务入账；送礼用 `gift_id` 主键加条件扣币，检查和扣减是一条原子语句；发件箱到事件流至少一次，消费者按 gift_id 去重。
**为什么不用别的。** Kafka 事务不覆盖钱包库；两阶段提交把可用性耦合起来且主播账户是热点。
**崩溃点。** 提交前崩溃客户端重试；提交后回复前崩溃，重试读到已保存结果；投递前崩溃，重启继续，下游靠去重吸收。
