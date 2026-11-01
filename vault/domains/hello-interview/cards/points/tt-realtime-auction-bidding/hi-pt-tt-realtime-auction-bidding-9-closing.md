---
id: hi-pt-tt-realtime-auction-bidding-9-closing
node: tt.sd.tt-realtime-auction-bidding.points
type: qa
step: 9
---
## Q
**实时竞价拍卖 · 结束时刻与防狙击**｜出自：实时竞价拍卖 › 深入 4

结束时间前后几百毫秒出价最密集，「到底算不算数」由谁裁决？防狙击怎么做？

## A
**裁决。** 拥有者以接收时的服务端时间与 `end_at` 比较；关闭与出价在同一串行化点；数据库条件更新带 `status = 'open'` 与 `now() < end_at`，实例时钟有偏差也能拦住。
**防狙击。** 最后 30 秒内有新出价就顺延 30 秒，最多若干次，同样是拥有者写 `end_at` 的事务并推送新结束时间。
