# followups · 第二部分：扩展 + 规模

原话（#8496901）：Concurrency · Parallelism · Worker scaling · Message queue scaling · Throughput · Bottlenecks · Failure scenarios；"be prepared to go beyond 'add more workers' or 'use a queue.'" 这个题的"规模"主要落在 **缓存、数据库、分页和多租户公平性**上。每题：中文要点 + 英文口播。数字都用 `python3 -c` 算过，面试时换成自己的假设并现场算。

## F1 吞吐估算：一个读多写少的 API

- 假设峰值 500 req/s，缓存命中率 95% → 回源 25 次/s；每次回源 2 条 SQL → **50 条查询/s**，对 Postgres 很轻松。
- 但命中率从 95% 掉到 50%（Redis 重启、批量过期）→ 回源 250/s、500 条查询/s：容量要按**冷缓存**设计，而不是按稳态。
- 进程容量：`wsgiref` 单线程，每请求 30 ms → 33 req/s；gunicorn 4 个 worker ≈ **133 req/s**，要 500 req/s 需要约 15 个 worker，或异步/多实例。
> "Steady state the database sees about 25 loads a second, which is nothing. The number I design for is the cold-cache case: if the hit rate drops from 95 to 50 percent, that's ten times the database traffic, so I size the database and the connection pool for that, not for the average."

## F2 缓存击穿、穿透、雪崩（三个不同的问题）

- **击穿**（热点 key 过期）：单进程内 single-flight（本题的分段锁）；多进程/多 pod 用 Redis `SET key NX EX 5` 当租约，没抢到的等待或返回旧值。注意进程内锁只把"每个请求回源"降到"每个 pod 回源一次"（20 个 pod = 20 次）。
- **穿透**（查不存在的 key）：对"用户不存在"做**负缓存**（短 TTL），否则攻击者用随机 id 可以绕过缓存直打 DB。
- **雪崩**（大量 key 同时过期）：TTL 加随机抖动（±10-20%）。例：1 万个 key 同时写入、TTL 300 s，等于在同一秒产生 33 次/s 的持续回源。
- 更进一步：**stale-while-revalidate**——过期后先返回旧值，后台刷新一次。
> "Three different failure modes: a hot key expiring, lookups for keys that don't exist, and many keys expiring together. I'd use a lease per key for the first, short negative caching for the second, and jittered TTLs plus serve-stale-while-revalidate for the third."

## F3 热点 key 的放大：计算一下

- 控制台对同一用户 200 req/s 轮询。回源耗时 50 ms → 过期瞬间并发回源 200 × 0.05 = **10 个**；回源耗时因 DB 变慢涨到 2 s → **400 个**，超过连接池，请求排队，耗时更长——正反馈。
- 所以 single-flight 的价值在"DB 慢的时候"最大，这正是最不能再加压的时候。
> "A hot key is a positive feedback loop: if the load takes longer, more requests pile up behind it. With 200 requests a second and a 2-second load, that's 400 concurrent loads on one key. A single-flight lease turns that into one."

## F4 分页在规模下的行为

- offset 分页翻到第 1000 页（每页 50）要扫 5 万行再丢弃，且翻页期间有插入/删除会重复或漏行；**keyset** 分页成本与页数无关，并稳定。
- 索引：`(tenant_id, risk_score, user_id)` 才能让 `ORDER BY risk_score, user_id` 不排序；否则每页一次文件排序。
- 非唯一排序键必须带唯一 tie-breaker（`user_id`），否则相同分数的行会重复/丢失（CR-07 的第二个测试）。
- 总数 `COUNT(*)` 在大表上贵：不返回总数，或返回近似值。
> "I'd keep keyset pagination, because its cost doesn't grow with the page number, add a composite index that matches the sort, always include a unique tie-breaker, and not return an exact total on large tenants."

## F5 一个租户拖垮所有人：公平性与限流

- 大租户一次导出 100 万用户，占满连接池；小租户的请求排队。对策：按租户（或按 key）限流（令牌桶），`limit` 上限（CR-08），并发上限（bulkhead），重查询走只读副本。
- 限流存哪：每个 pod 本地近似（`rate/pods`）或 Redis 计数（精确但多一次往返）。
- 返回 429 + `Retry-After`，客户端指数退避。
> "I'd rate-limit per tenant and per key with a token bucket, cap the page size, and give expensive exports their own lane, so one tenant's big export cannot starve the others' dashboards."

## F6 认证在规模下

- 每个请求查 `api_keys` 表是额外一次 DB 往返；可缓存 `key_id → (tenant, hash)` 60 s（含负缓存）。代价：吊销最长延迟 60 s——要和安全团队对齐，或用 pub/sub 主动失效。
- 常量时间比较 + 不存在的 key 也做一次比较，避免通过响应时间枚举有效 `key_id`。
> "Caching key lookups saves a database round trip per request, but it makes revocation eventually consistent, so I'd cap that at a minute, or invalidate on revoke, and agree it with security."

## F7 失败场景

- Redis 宕机：缓存是优化而非依赖——`get` 失败当 miss，但此时全部回源 → 需要**降级**（限流 / 返回稍旧的本地缓存 / 熔断），否则缓存故障变成 DB 故障。
- DB 慢/不可用：超时 + 熔断；对已缓存的用户继续服务（serve stale）。
- 缓存被投毒（CR-03）：json + 校验 schema；坏数据当 miss 并告警。
- 部分租户数据迁移：缓存 key 带版本号（`risk:v2:...`），发布时换版本而不是清空。
> "I treat the cache as an optimisation, never a dependency: if Redis is down we fall back to the database, but we also shed load, otherwise a cache outage becomes a database outage."

## F8 缓存一致性：什么时候更新

- 评分是夜间作业写入（`rescore.py`），API 缓存 5 分钟 → 最长陈旧 5 分钟 + 作业延迟。
- 选项：TTL（简单）；作业完成后按租户批量 `delete`/换版本号；事件驱动（Kafka 上的 score-updated 事件触发失效）。
- 先问产品：控制台能接受多陈旧？SLO 是"评分更新后 1 分钟内可见"还是"5 分钟"？
> "I'd first ask what staleness the product tolerates. If five minutes is fine, TTL is enough; if not, the scoring job emits an event per user and the API invalidates that key, which is cheap because the key includes the tenant."

## F9 横向扩展 API 进程

- API 无状态，可水平扩展；瓶颈转移到：DB 连接数（`workers × pool_size ≤ max_connections`，如 20 pods × 4 workers × 5 连接 = 400 > Postgres 默认 100，需要 pgbouncer）、Redis 连接与带宽、单个热点 key（Redis 单分片）。
- 热 key 的 Redis 层对策：本地进程内小 TTL 二级缓存（1-2 s）、key 复制多份。
> "Adding pods is easy because the API is stateless; the constraint moves to database connections. Twenty pods times four workers times five connections is four hundred, so I'd put a pooler in front of Postgres before adding more."

## F10 观测

- 指标：QPS、p50/p99 延迟（按路由）、缓存命中率、回源次数、single-flight 等待数、DB 连接池使用率、429/4xx/5xx 比例（按租户）、分页深度分布。
- 告警：命中率骤降、p99 > SLO、连接池使用率 > 80%、某租户 4xx 突增（可能在探测 IDOR，CR-01 之后 404 的突增也是信号）。
- 日志：结构化，tenant/user id/路由/状态/耗时；**不含 PII**（CR-09）。
> "I'd watch hit rate and database load together, because a falling hit rate is the leading indicator for a database incident, and I'd alert on a spike of 404s for one key, since that is what someone probing other tenants looks like."
