---
id: hi-pt-tt-per-merchant-rate-limit-8-multi-instance
node: tt.lld.tt-per-merchant-rate-limit.points
type: qa
step: 8
---
## Q
**按商户限流 · 多实例部署**｜追问 · 出自：按商户限流 › 取舍与追问

限流器部署多个实例时有哪两种做法？各自的代价是什么？

## A
**Redis。** 把桶放进 Redis，用一个 Lua 脚本原子完成读状态、补充、扣减、写回。
**一致性哈希。** 按商户 ID 把同一商户的请求路由到固定实例，桶留本地内存，延迟最低；代价是实例变动时桶要迁移或重置。
