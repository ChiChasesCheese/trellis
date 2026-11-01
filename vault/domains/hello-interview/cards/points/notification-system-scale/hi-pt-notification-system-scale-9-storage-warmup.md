---
id: hi-pt-notification-system-scale-9-storage-warmup
node: qb.sd.notification-system-scale.points
type: qa
step: 9
---
## Q
**百万级通知系统 · 存储与大促预热**｜出自：百万级通知系统 › 深入 6

通知系统的投递记录、偏好、模板、设备令牌怎么选存储？大促前要注意什么？

## A
**投递记录。** 写多读少，宽列存储（Cassandra）或分片 KV，主键 (user_id, 时间倒序)，TTL 30 到 90 天。
**偏好与模板。** 读多写少，关系库加缓存。
**预热与降级。** 偏好缓存必须预热，否则穿透打垮偏好库；偏好服务宕机时关键通知默认放行，促销默认不发。
