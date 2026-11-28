---
id: hi-c-sd-distributed-rate-limiter-n05-client-identity
node: sd.problem-breakdowns.distributed-rate-limiter.notes
type: qa
step: 5
---
## Q
**分布式限流器 · 怎么识别客户端与叠加规则**｜摘要 · 必会

网关只能看到请求本身，客户端用什么标识？多条规则同时适用时怎么判定？

## A
- **只看请求本身：** 网关可用的信息是路径、请求头、查询参数、来源 IP。技术上能查库，但会增加想避免的延迟，所以不用。
- **三种标识：**
  - 用户 ID：适合有登录的 API，通常来自 `Authorization` 里的 JWT；
  - IP 地址：适合公开 API 或没有账号时，来自 `X-Forwarded-For`；但 NAT、公司防火墙后很多人共用同一个 IP，容易误伤；
  - API key：开发者 API 常用，在 `X-API-Key` 头里。
- **现实是组合：** 登录用户限额高于匿名 IP，付费用户更高。因此同时存在多层规则：每用户（"Alice 每小时 1000 次"）、每 IP（"每分钟 100 次"）、全局（"整个 API 每秒 5 万次"）、特定端点（搜索每分钟 10 次，资料更新每分钟 100 次）。
- **判定：** 检查所有适用规则，执行最严格的一条。Alice 的 1000 次只用了 50，但她的 IP 已达每分钟 100 次，也要拦住。
- **面试里：** 这是向面试官提问的好时机：用户都登录了吗？是需要 API key 的开发者 API 吗？
