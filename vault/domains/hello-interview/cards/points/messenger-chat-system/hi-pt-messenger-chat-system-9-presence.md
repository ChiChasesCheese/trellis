---
id: hi-pt-messenger-chat-system-9-presence
node: qb.sd.messenger-chat-system.points
type: qa
step: 9
---
## Q
**聊天与即时通讯系统 · 在线状态与输入中提示**｜出自：聊天与即时通讯系统 › 深入 5

在线状态和「正在输入」怎么做才不引发扇出爆炸？

## A
**在线。** 存 Redis，心跳每 30 秒刷新 TTL，90 秒不刷新视为离线，不进持久库。
**不要。** 上下线时通知所有联系人；改成只有对方打开了与你的会话页面才订阅你的状态。
**输入中。** 只发给当前会话在线成员，不持久化、限频。
