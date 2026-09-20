---
id: problems-notification-system-digest-reduction
node: problems.social.notification-system
type: qa
step: 5
tags: [grown]
---
## Q
A post receives 500 likes in one hour. If a notification system batches likes on the same post into one digest notification per 10-minute window instead of sending one notification per like, how many notifications does the author receive that hour, and what is the reduction factor?

## A
60 minutes / 10-minute window = 6 windows, so at most 6 digest notifications are sent that hour (each summarizing "N people liked your post" for that window), versus 500 if every like triggered its own notification — a reduction of about 83x (500/6). This batching only applies to notification types marked mergeable by the triggering business logic (social interactions like likes and follows); transactional notifications (OTP, order confirmations) are never digested because each one is individually time-critical.

## Q zh
一篇帖子在一小时内收到 500 个赞。如果通知系统把同一帖子的赞合并成每 10 分钟一条摘要通知，而不是每个赞都单独发一条，作者这一小时会收到多少条通知？降低了多少倍？

## A zh
60 分钟 / 10 分钟一个窗口 = 6 个窗口，所以这一小时最多发出 6 条摘要通知（每条汇总该窗口内"N 人赞了你的帖子"），相比每个赞都单独触发通知的 500 条，降低了约 83 倍（500/6）。这种合并只适用于触发端业务逻辑标记为可合并的通知类型（点赞、关注等社交互动）；事务性通知（OTP、订单确认）永远不合并，因为每一条都是单独时效关键的。
