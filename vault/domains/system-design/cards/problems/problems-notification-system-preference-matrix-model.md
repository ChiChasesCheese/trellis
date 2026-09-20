---
id: problems-notification-system-preference-matrix-model
node: problems.social.notification-system
type: qa
step: 2
tags: [grown]
---
## Q
Why does a notification system model user preferences as a (notificationType, channel) matrix rather than a single per-user channel toggle (e.g. "push: on, email: off")?

## A
A single global channel toggle can't express that a user wants push for security alerts but not for "someone liked your post" — both are the same channel but very different notification types. Storing preference as (userId, notificationType, channel, enabled) lets each notification type be independently enabled or disabled per channel, so a user can silence low-value social notifications on push while keeping security alerts on every channel. It also lets the system apply a different default policy per type (e.g. security notifications default to all channels on and are not user-overridable, while social notifications default to a subset).

## Q zh
为什么通知系统把用户偏好建模为（通知类型，渠道）二维矩阵，而不是单一的每用户渠道开关（比如"push: 开，email: 关"）？

## A zh
单一的全局渠道开关无法表达"用户想要安全提醒走 push，但不想要'有人赞了你的帖子'也走 push"——两者是同一个渠道，但通知类型完全不同。把偏好存成 (userId, notificationType, channel, enabled) 让每种通知类型可以在每个渠道上独立启用/禁用，用户可以在 push 上屏蔽低价值的社交通知，同时在所有渠道上保留安全提醒。这也让系统可以对不同类型套用不同的默认策略（例如安全通知默认全渠道开启且用户不可关闭，社交通知默认只开一部分）。
