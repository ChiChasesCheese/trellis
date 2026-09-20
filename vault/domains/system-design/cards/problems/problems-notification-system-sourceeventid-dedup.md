---
id: problems-notification-system-sourceeventid-dedup
node: problems.social.notification-system
type: qa
step: 3
tags: [grown]
---
## Q
In a notification system, what should a business service pass as the idempotency key when triggering a notification, and why must it be tied to the business event rather than generated fresh on every HTTP call?

## A
The business service passes a `sourceEventId` that identifies the underlying event itself — e.g. "order 123 transitioned to shipped" — reused across every retry of that same trigger, never a new UUID minted per HTTP attempt. The notification API performs a unique-constraint write of `sourceEventId` into a dedup store before enqueueing; a write conflict means the event was already processed, so the API returns the existing notificationId instead of enqueueing a second one. If the key were regenerated per request, a client-side retry after a network timeout would look like a brand-new event and the same notification would be sent twice.

## Q zh
在通知系统中，业务服务触发一条通知时应该传什么作为幂等键，为什么它必须绑定业务事件本身，而不是每次 HTTP 调用时新生成一个？

## A zh
业务服务传递一个标识底层事件本身的 `sourceEventId`——例如"订单 123 状态变更为已发货"——同一触发的每次重试都复用这同一个值，绝不是每次 HTTP 尝试铸造一个新 UUID。通知 API 在入队之前先对 `sourceEventId` 在去重存储上做一次唯一约束写入；写入冲突意味着该事件已经处理过，API 直接返回已有的 notificationId，而不会再入队第二条。如果 key 每次请求都重新生成，网络超时后的客户端重试就会看起来像一个全新事件，同一条通知会被发送两次。
