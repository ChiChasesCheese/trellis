---
id: problems-notification-service-transient-vs-permanent
node: problems.components.notification-service
type: qa
step: 6
tags: [grown]
---
## Q
通知服务的渠道发送失败。为什么必须把失败分成两类？分别怎么处理？用什么承载这个区分？

## A
两类是**瞬时失败**（超时、502、对端限流——再试一次也许就好）和**永久失败**（地址非法、用户已注销、内容被拒——重试一百次也是同一个结果）。不区分它们，要么把永久失败按指数退避重试五次、白白浪费，要么把一次网络抖动一次就丢进死信。

承载这个区分的是**异常类型**：渠道抛 `TransientDeliveryError` 表示可重试，抛 `PermanentDeliveryError`（或任何其他异常）表示不可重试。派发器据此分流：前者按退避排进重试，次数用尽才进死信；后者直接进死信。

配套的还有结果状态不能合成一句『失败』：调用方拿到『触发限额』会知道稍后再试有用，拿到『渠道被用户关掉』会知道别再试了、去提示用户改设置，拿到『已进死信』会知道这事需要人来看。
