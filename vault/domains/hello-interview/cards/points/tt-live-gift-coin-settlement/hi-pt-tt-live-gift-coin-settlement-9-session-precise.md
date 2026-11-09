---
id: hi-pt-tt-live-gift-coin-settlement-9-session-precise
node: tt.sd.tt-live-gift-coin-settlement.points
type: qa
step: 8
---
## Q
**直播礼物金币记账与主播结算 · 每场精确收益与取整**｜必会 · 出自：直播礼物金币记账与主播结算 › 深入 3

每场直播的收益实时是估计、事后要精确。session 归属怎么定？批处理怎么重算？7 个币 35% 为什么不能逐份取整？

## A
**归属。** `session_id` 由礼物服务扣币时按房间当前场次盖章，客户端不能选也不能事后改。
**重算。** 场次结束过水位线（如 30 分钟）后，批处理按 session_id 从事件湖重算：按 gift_id 去重、排除已撤销、累加 share_micro，覆盖流式结果，差异超阈值报警。
**取整。** 7×35%=2.45，逐份向下取整成 2，每份损失 0.45，占 18.4%，14 亿份累成系统性误差。全程用 micro 整数累加，周期汇总值向下取整一次，余数记入下一周期。
