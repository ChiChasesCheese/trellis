# 模型答案：设计 Webhook 投递系统

> 取材：Emily 一手面经（Medium，2026-05-20，Staff 面试官）；Stripe 官方 webhooks 文档；systemdesignhandbook《Design a Webhook System》；Svix webhook 综述；`loop/raw/system_design.md` §4.1。按 `LOOP_GUIDE.md` §7 主线组织。

## 0. 两句话复述 + 不变量

**复述**：内部各业务系统产生事件（付款成功、退款到账、账户被冻结……）之后，我们需要把这些事件可靠地投递给商户在自己后台注册的一个或多个 HTTPS 端点；商户的端点是完全不受我们控制的外部系统，可能很快、很慢、会挂、甚至有恶意，我们必须在这种不可信的前提下做到"接受了就尽力送到"，同时不能让一个坏商户拖垮其他所有商户的体验。

**核心不变量**（面试一开始就要说出来，后面所有设计决策都要能回溯到这几条）：

1. **至少一次投递**：一个事件一旦被系统接受（写入了 events 表），就必须被尝试投递，直到成功或者明确进入死信（DLQ）。
2. **不保证顺序、不保证 exactly-once**：网络本质上做不到端到端 exactly-once，我们提供的是 at-least-once + 商户侧幂等去重的组合等价物。
3. **租户隔离**：任何一个商户端点的行为（慢、挂、恶意）都不能影响到别的商户收通知的时效性。
4. **不可变审计**：事件内容一旦生成不再修改，每一次投递尝试都要留痕，方便商户和我们自己排查。

明确"不做什么"同样重要：不做严格全局顺序保证；不做端到端 exactly-once；不承诺商户端点在任意情况下都能收到（网络分区/商户长期宕机时最终会放弃）。

## 1. API 契约

商户侧管理 API（同步、幂等、版本化）：

```
POST   /v1/webhook_endpoints        {url, enabled_events[], description}
                                     → {id, secret: "whsec_...", status: "active"}
GET    /v1/webhook_endpoints/:id
POST   /v1/webhook_endpoints/:id    {enabled_events?, disabled?}   # 更新用 PATCH 语义
DELETE /v1/webhook_endpoints/:id

GET    /v1/events?type=&created[gte]=&cursor=&limit=   # 补漏拉取，游标分页
POST   /v1/events/:id/resend?endpoint=                  # 手动重发，创建后 N 天内有效
GET    /v1/events/:id/deliveries                        # 某个事件在各端点的投递历史
```

出站请求契约（我们主动发给商户的那个 POST）：

```
POST {商户注册的 url}
Headers:
  Content-Type: application/json
  Stripe-Signature: t=<unix_ts>,v1=<HMAC-SHA256(secret, "{t}.{raw_body}")>
Body（Event 对象，创建后不再变化）:
  {id: "evt_...", type: "payment_intent.succeeded", created, api_version, livemode, data: {object: {...}}}
```

契约细则（这些是面试官爱追问的边界）：

- 每个账户最多注册若干个 endpoint（有限额，防止滥用），每个 endpoint 只对自己订阅的 `enabled_events` 生效。
- 仅接受 TLS ≥ 1.2 的 https 地址；3xx 一律视为投递失败，**不自动跟随重定向**（这一点同时也是安全考虑，见失败处理一节）。
- 幂等键就是 `event.id`：同一个事件多次投递（重试导致的）body 里的 `id` 完全一致，商户按这个字段去重。
- 版本：Event 的结构由账户当时 pin 的 API 版本决定，一旦生成不再跟随账户以后升级版本而改变；请求头允许显式覆盖版本用于联调。
- 错误响应没有固定格式要求（对方是商户自己的系统），但我们自己对商户管理 API 的错误要结构化：`{error:{type, code, message, param}}`。
- 分页：`GET /v1/events` 用 cursor（`starting_after`/`ending_before`）而不是 offset，避免深分页时事件表被全表扫描。

## 2. 数据模型

区分**可变配置对象**与**不可变事实记录**是这道题数据建模的核心：

```
webhook_endpoints(
  id, account_id, url, enabled_events[], status[active|disabled],
  secret_current, secret_previous, secret_previous_expires_at,
  api_version, created_at
)
-- 可变：商户随时可以改 url/enabled_events/禁用
-- 密钥轮换期新旧 secret 并存一段时间（如 24h），两把密钥各自签一份 v1 签名，
--   避免商户还没切换完新密钥时旧签名验证突然失败

events(
  id, account_id, type, payload jsonb, api_version, created_at
)
-- 不可变，是这个系统的"事实源"；按当时 pin 的 api_version 生成一次，之后不改

deliveries(
  id, event_id, endpoint_id,
  status[pending|succeeded|failed|dead],
  attempt_count, next_attempt_at, last_response_code,
  created_at
)
-- 每个 (event, endpoint) 组合一行；索引 (status, next_attempt_at) 供调度器扫描

delivery_attempts(
  id, delivery_id, attempted_at, response_code,
  response_snippet, duration_ms, error
)
-- 每次真实发出去的 HTTP 请求一行，商户在 Dashboard 看到的"投递历史"就是这张表

dead_letters(delivery_id, all_attempts jsonb, created_at)
-- 超过最大重试次数/时间窗后落地，供人工介入或商户主动 resend
```

金额或计数类字段这里不多，重点是**审计链条完整**：`events` → `deliveries` → `delivery_attempts` 三层，任何一次投递的来龙去脉都能重建。

## 3. 一致性 / 幂等

- **事件产生的一致性**：业务系统在同一个数据库事务里写自己的业务状态和一条 outbox 记录（outbox pattern），由一个 relay 进程把 outbox 里的记录发布到消息队列（如 Kafka），保证"业务状态改了就一定有对应事件产生"，不会因为进程崩溃在中间丢事件。
- **匹配与生成投递记录**：Dispatcher 消费事件流，查询该账户的 `webhook_endpoints`（这一步走 Redis 缓存 `endpoints:{account}:{type}`，因为端点配置变更频率远低于事件产生频率，是典型的"慢路径缓存，快路径读缓存"）；为每个匹配的端点插入一条 `deliveries(pending)`。这一步要做到**幂等**（同一个事件不会因为 Dispatcher 重复消费而生成两条 deliveries）——用 `(event_id, endpoint_id)` 唯一约束。
- **投递去重**：DB 唯一约束才是真相源，Redis 只是加速匹配查询，不参与去重判断；即便 Redis 缓存脏了导致 Dispatcher 重复处理，唯一约束也会挡住重复的 `deliveries` 行。
- **商户端幂等**：我们能做的只是把 `event.id` 稳定不变地带给商户，剩下"收到重复 event.id 就跳过"是商户自己的责任，我们在文档里明确要求这一点。

## 4. 失败处理

这是这道题被压分最重的一节，Staff 面试官的拒因原话就是"failure domains and system abuse"，下面逐条覆盖：

**重试 / 退避 / 抖动**：

```
delay = base × 2^attempt × (1 + jitter)   # jitter 防止大量失败同时重试造成 thundering herd
序列示例：1min → 5min → 30min → 2h → 8h → 24h，最长持续到 3 天后放弃
```

三天后仍未成功 → 该 delivery 转 `dead`，落 DLQ，通知商户，达到一定失败率时可自动禁用该 endpoint（避免继续浪费资源在一个显然坏掉的端点上）。

**噪声邻居（noisy neighbor）**：如果不做隔离，一个响应慢/挂起 30 秒的商户端点会占满 worker 的连接和线程，导致其他商户的事件也排不上队。对策：
- per-endpoint 并发上限（例如同一个 endpoint 同时只允许 ≤20 个在途请求）；
- per-tenant 的队列或令牌桶，保证调度层面上不会被一个商户占满全局资源；
- 连接池按租户隔离，避免慢连接占用全局连接池。

**熔断**：某个 endpoint 连续失败次数或失败率超过阈值时，进入"open"状态——后续事件直接进延迟队列，不再占用 worker 尝试，定期"半开"探测恢复；恢复后才逐步放量。

**超时设置**：连接超时 2 秒、读超时 5 秒；超时一律视为失败进入重试流程，不会无限期占用 worker。

**SSRF / DNS rebinding**（Staff 拒因点名的另一半）：商户填的 URL 本质上是不可信输入。风险是：注册时校验域名解析到公网 IP，但真正投递时该域名的 DNS TTL 过期、重新解析到了内网地址或云 metadata 服务（169.254.169.254 之类），从而让我们的服务器变成攻击者访问内网的跳板。对策：
- 注册/更新 endpoint 时解析域名，拒绝解析到私网段、保留段、云 metadata 地址的 URL；
- **真正发起请求时，使用注册时校验通过的 IP 直连**，Host 头带原始域名（而不是每次投递都重新走 DNS 解析），从根上切断 TTL 过期后被"rebind"到内网的路径；
- 禁止跟随任何 3xx 重定向（重定向目标同样可能指向内网）；
- 出站流量走独立的 egress 网段/代理，即便校验百密一疏也把爆炸半径限制在一个隔离的网络里。

**exactly-once 能不能做到**：不能。网络的基本事实是，我们发出请求后，如果没在超时内收到响应，我们无法区分"商户没收到"和"商户收到了但响应丢了"，重试是唯一安全的默认动作，所以只能提供 at-least-once，配合商户按 `event.id` 去重达到业务上的等价效果。

**顺序保证**：默认不保证。如果面试官追问"商户坚持要顺序"，可以讨论按 `object_id` 做分区键、单 endpoint 单线程消费，代价是吞吐下降和 head-of-line blocking（一个卡住的事件会挡住同一分区后面所有事件），并建议商户更稳妥的做法是"收到事件后主动 GET 最新对象状态"而不是依赖事件顺序。

**背压**：队列消费延迟（lag）超过阈值触发 worker 自动扩容；队列深度报警防止无限堆积拖垮下游存储。

## 5. 对账 / 审计

- **商户侧补漏**：`GET /v1/events` 支持按时间范围拉取历史事件，商户可以定期核对"我本地处理过的 event.id 集合"和"我应该收到的 event.id 集合"之间的差集，主动 `resend` 缺失的。
- **平台侧对账**：每日批处理任务对比"应该生成的 deliveries 数量"（events × 匹配的 enabled endpoints）与"实际 succeeded 的数量"，差异超过阈值报警，用于发现 Dispatcher 或调度器本身的 bug，而不是依赖商户来发现我们系统的问题。
- **DLQ 复盘**：定期人工/自动化审查 DLQ 里的记录，区分"商户端点本身长期失效"和"我们这边有 bug 导致大批量失败"两类原因。

## 6. 可观测性 + rollout

**监控指标**：
- 全局与分商户的投递成功率（如 5 分钟窗口内失败率 > 5% 触发告警）；
- p99 首次投递尝试延迟（目标秒级，超过阈值报警）；
- 队列深度与消费 lag；
- DLQ 增长速率；
- 按 endpoint 维度的健康分（用于自动禁用长期失效端点的依据）。

**商户可见性**：Dashboard 展示每一次 `delivery_attempts` 的状态码、耗时、下一次重试时间，让商户自己能诊断"是我这边挂了还是 Stripe 没送"，减少支持工单。

**rollout / 上线策略**：
- 新的匹配逻辑或重试策略变更先以 **dark launch**（只记录不影响真实投递路径）方式跑一段时间，对比新旧逻辑的差异后再切流量；
- 密钥轮换等运维动作设计成"新旧并存"而不是"硬切"，避免和商户的部署节奏产生竞态；
- 全链路加 `request_id`/`event_id` 贯穿日志，方便一次投递失败时快速定位是匹配层、队列层还是 worker 层的问题；
- 灰度：先在低风险的事件类型或小流量商户上验证新版本 Dispatcher/Worker，再逐步扩大范围。

## 7. 规模估算（简要）

10k events/s，假设平均每个事件匹配 2 个 endpoint，则出站请求峰值约 20k POST/s；每条事件 payload 约 2KB，写入吞吐约 20MB/s；30 天留存对应约 50TB 量级，需要冷热分层存储（近期热数据在 OLTP，历史数据归档到对象存储/OLAP）。Worker 层无状态、按负载水平扩展；事件队列按 `account_id` 分区；`deliveries`/`delivery_attempts` 按时间分区并按 `endpoint_id` 分片，避免单表过大影响索引效率。
