---
id: problems-auth-service-token-verification-qps-forces-stateless
node: problems.foundations.auth-service
type: qa
step: 2
tags: [grown]
---
## Q
In an authentication service serving 150M DAU where token verification (with internal service fan-out) can peak around 1.7 million checks/sec, why does this number rule out a pure server-side session store as the default verification mechanism?

## A
A single Redis-class primary is assumed to sustain on the order of tens of thousands of operations per second (say 50,000/sec). At a 1.7M QPS peak, a pure session-lookup approach would need roughly 35 independent shards just for verification checks — on top of whatever else each shard already handles. That number is the concrete reason to make the access token a short-lived, stateless JWT verified locally against a cached public key (zero network round trip), pushing revocation to a separate, rarely-touched refresh-token flow instead of touching a central store on every request.

## Q zh
在一个服务 1.5 亿日活、令牌验证（含内部服务扇出）峰值约 170 万次/秒的认证服务中，为什么这个数字排除了把纯服务端会话存储作为默认验证机制？

## A zh
一个 Redis 一类的单一主节点被假设能承受量级约数万次操作/秒（比如 50,000/秒）。在 170 万 QPS 峰值下，纯会话查找方案需要约 35 个独立分片仅用于验证检查——还不算每个分片本来就要承担的其它负载。这个数字是把 access token 做成短生命周期、本地校验(零网络往返)的无状态 JWT 的具体依据，把撤销推到一个独立的、很少被触碰的 refresh token 流程里，而不是每个请求都碰一次中心化存储。
