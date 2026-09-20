---
id: problems-notification-system-preference-service-outage-degradation
node: problems.social.notification-system
type: qa
step: 7
tags: [grown]
---
## Q
If the preference-and-quiet-hours service becomes unavailable in a notification system, why should transactional notifications and marketing notifications degrade in opposite directions?

## A
Transactional notifications (OTP, security alerts) skip the preference/quiet-hours check entirely and send on the default channel set — the cost of sending one extra unwanted transactional message is far lower than the cost of a missed security alert or login code, so availability wins over honoring preferences. Marketing notifications instead defer sending until the preference service recovers, because sending a marketing message that ignores a user's quiet hours or opted-out channel has a real trust cost, while a delayed marketing message loses little value. Neither notification type simply fails outright — the failure mode is chosen per notification type based on which error (send late, or send without checking preferences) is cheaper.

## Q zh
如果通知系统的偏好与免打扰服务不可用，为什么事务性通知和营销通知应该朝相反方向降级？

## A zh
事务性通知（OTP、安全提醒）完全跳过偏好/免打扰检查，按默认渠道集合直接发送——多发一条不想要的事务性消息的代价，远低于漏发一条安全提醒或登录验证码的代价，所以可用性优先于遵守偏好。营销通知则相反，推迟发送直到偏好服务恢复，因为发出一条无视用户免打扰设置或已退订渠道的营销消息有真实的信任成本，而营销消息延迟发送几乎不损失价值。两种通知类型都不是简单地直接失败——降级方式是按通知类型选择哪种错误（晚发，还是不查偏好就发）代价更低。
