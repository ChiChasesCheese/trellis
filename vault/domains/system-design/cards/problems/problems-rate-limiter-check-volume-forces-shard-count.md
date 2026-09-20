---
id: problems-rate-limiter-check-volume-forces-shard-count
node: problems.foundations.rate-limiter
type: qa
step: 1
tags: [grown]
---
## Q
In a rate limiter design with a 20-gateway fleet averaging 100,000 req/s (peak 300,000 req/s at a 3x diurnal factor) where every request must pass three independent limit checks (per-key sustained, per-key burst, per-endpoint), why does a fully synchronous 'check every request against a central Redis store' design need on the order of 14 Redis shards at peak, not 1 or 2?

## A
Three checks per request at 300,000 req/s peak gives 900,000 rate-limit checks/second. Budgeting conservatively for about 100,000 atomic Lua-script operations per Redis shard per second, covering that volume needs ceil(900,000/100,000)=9 shards with zero redundancy, or ceil(900,000/100,000*1.5)=14 shards with 1.5x headroom for failover and uneven load. The number of shards is driven by operation throughput, not by how many keys exist or how much memory the counters use.

## Q zh
在一个速率限制器设计中，20 台网关组成的集群均值 100,000 req/s（日间峰值系数 3，峰值 300,000 req/s），每个请求都要通过三层独立的限流检查（per-key sustained、per-key burst、per-endpoint），为什么一个'每个请求都同步查中心 Redis'的设计在峰值下需要大约 14 个 Redis 分片，而不是 1 个或 2 个？

## A zh
每个请求 3 次检查，峰值 300,000 req/s 意味着每秒 900,000 次限流检查。保守估计单个 Redis 分片每秒能稳定承载约 100,000 次原子 Lua 脚本操作，覆盖这个量级需要 ceil(900,000/100,000)=9 个零冗余分片，或者 ceil(900,000/100,000×1.5)=14 个含 1.5 倍冗余（故障转移和负载不均）的分片。分片数量由操作吞吐量决定，与 key 的总数或计数器占用的内存无关。
