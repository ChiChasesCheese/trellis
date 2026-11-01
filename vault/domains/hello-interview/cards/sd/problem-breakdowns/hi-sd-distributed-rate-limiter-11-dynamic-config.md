---
id: hi-sd-distributed-rate-limiter-11-dynamic-config
node: sd.problem-breakdowns.distributed-rate-limiter
type: qa
step: 11
---
## Q
**动态规则配置：轮询还是推送**｜系统设计 · 问题拆解

限额规则要能不发版就调整，有哪两种做法？各自的延迟和复杂度代价是什么？

## A
**轮询（常用）。** 规则存数据库或配置服务（如表里有 client_type、endpoint、requests_per_minute），网关每 30 秒左右拉一次，本地缓存。简单，覆盖大多数场景。代价：改规则到全网关生效有延迟，遇到攻击想紧急降限额，最多要等 30 秒。

**推送（更强）。** 配置变更立即推给所有网关，几秒内生效。ZooKeeper 就是为此设计的（分布式配置加实时通知），Redis pub/sub 或自建的长连接配置服务也行。代价：要处理连接故障、保证所有网关收到、部分成功部分失败，还需要推送不可用时的兜底。

**选择。** 推送的运维复杂度通常只在需要极快更新的系统才值得，比如处理安全事件或高频交易。多数情况轮询足够。
