---
id: amz-rate-limiter-distributed-and-naive-break
node: amazon.amz-rate-limiter
type: qa
step: 6
tags: [grown]
---
## Q
在限流器设计里，部署到多台机器后，「每台机器各自限 100 次/分钟」为什么错？共享额度有哪两种做法？

## A
3 台机器各限 100，整体最多放行 300，且负载均衡不均时单个用户的上限不可预测。做法一：集中计数——Redis 用 Lua 脚本原子地「读计数、判定、自增并设过期」，精确，但每个请求多一次网络往返，Redis 故障要决定放行还是拒绝（fail-open / fail-closed）。做法二：中央租约——每台机器向中心批量领一份额度（如 20 个令牌）本地花，用完再领，延迟低，代价是额度在机器间有浪费、精度变粗。
