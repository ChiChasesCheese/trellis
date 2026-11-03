---
id: hi-pt-distributed-rate-limiter-8-hot-key
node: qb.sd.distributed-rate-limiter.points
type: qa
step: 8
---
## Q
**分布式限流器 · 热点客户端**｜追问 · 出自：分布式限流器 › 深入 5

分布式限流器里单个客户端的请求量大到能压垮一个 Redis 分片。合法大客户和恶意流量分别怎么处理？

## A
**合法大客户。** 要求客户端自己限流并遵守响应头，批量接口减少调用，付费大客户更高限额，必要时专用分片。
**恶意流量。** 连续超限若干次后进封禁列表，网关本地缓存几秒先查，不用每次打 Redis；更上游由 CDN、DDoS 防护拦截。
**共享 IP。** 公司 NAT 和公共 Wi-Fi 让多人共用一个 IP，IP 限额一开始就放宽，主要靠认证后的用户限额。
