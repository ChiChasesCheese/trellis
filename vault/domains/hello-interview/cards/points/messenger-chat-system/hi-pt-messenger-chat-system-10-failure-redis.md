---
id: hi-pt-messenger-chat-system-10-failure-redis
node: qb.sd.messenger-chat-system.points
type: qa
step: 10
---
## Q
**聊天与即时通讯系统 · 故障兜底：Redis 与网关宕机**｜追问 · 出自：聊天与即时通讯系统 › 取舍与追问

追问：Redis 挂了、网关机器宕机，消息会丢吗？

## A
**Redis。** 会话目录可重建（网关重新注册本机所有连接），发布订阅丢消息由收件箱兜底，所以只影响延迟不影响正确性。
**网关。** 客户端检测断开 → 重连另一台 → 带 `cursor` 补收；旧连接记录靠 TTL 过期。
