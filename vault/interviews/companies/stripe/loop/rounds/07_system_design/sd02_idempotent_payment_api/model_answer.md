# 模型答案：设计幂等的支付 / Charge API

> 取材：Stripe《Designing robust and predictable APIs with idempotency》（2017）；Stripe 文档 Idempotent requests；brandur《Implementing Stripe-like Idempotency Keys in Postgres》；Medium h7w（2026-04-03）；`loop/raw/system_design.md` §4.2。按 `LOOP_GUIDE.md` §7 主线组织。

## 0. 两句话复述 + 不变量

**复述**：商户调用我们的核心收款接口对一张卡发起扣款，商户端网络环境不可控，同一笔业务意图可能因为超时/重试被重复发送多次 HTTP 请求（可能打到我们不同的机器实例上）；我们必须保证这些重复请求最终只对应**至多一次**真正的外部扣款，同时不能因为过度保守而把本该成功的请求错误地标记为失败。

**核心不变量**：

1. **一个幂等键 ↔ 至多一次外部扣款**：无论重试多少次、打到哪台机器，同一个 `Idempotency-Key` 最终只会真正触发一次对卡组织的授权调用。
2. **不丢单**：一个被接受的请求，最终一定有一个确定性的结果（成功/失败/需要用户操作），不会永远卡在"不确定"状态而不给出解决路径。
3. **金额精确**：一律用整数最小货币单位（如分）存储和传输，不使用浮点数，避免精度问题。
4. **记账与授权状态最终一致**：授权成功之后一定有对应的记账记录，反之亦然，不允许"钱动了但账没记"或"账记了但钱没动"的中间态长期存在。

明确不做什么：不承诺对卡组织调用超时后能立刻告诉商户确切结果（可能需要走异步查询/对账收尾）；不允许同一幂等键但参数不同的请求被当作同一笔处理（视为客户端错误）。

## 1. API 契约

```
POST /v1/payment_intents
  Headers: Idempotency-Key: <uuid v4, ≤255 字符>, Stripe-Version: 2026-08-26
  Body: {amount(整数,最小货币单位), currency, payment_method, customer?,
         capture_method[automatic|manual], metadata{}}
  → 200 {id: "pi_...", status, amount, currency, client_secret, last_payment_error?}

POST /v1/payment_intents/:id/confirm     （幂等，同样要求 Idempotency-Key）
POST /v1/payment_intents/:id/capture     （手动 capture 场景）
POST /v1/payment_intents/:id/cancel
GET  /v1/payment_intents/:id
POST /v1/refunds  {payment_intent, amount?}  + Idempotency-Key
```

契约细则（面试官常追问的边界情况）：

- **幂等键的行为**：首次请求处理完成后，幂等层保存**首个请求的完整响应**（状态码 + body，即便是 5xx）；同一个 key 重放，直接返回当初保存的结果，不再重新执行业务逻辑。这一点很反直觉但很关键——如果只存"是否处理过"这个布尔值而不存响应内容，两次重放可能因为系统状态已经变化而返回不一致的结果，破坏幂等的语义。
- **同 key 不同参数**：视为客户端错误，返回 `idempotency_error`，不执行任何业务逻辑。
- **同 key 并发在途**：如果第一个请求还没处理完，第二个带着相同 key 的请求到达，应该返回"请求处理中，请稍后重试"（如 409），而不是让第二个请求也去发起一次外部调用。
- **幂等键只对写操作（POST）生效**，GET 类查询不需要。
- **错误结构**：`{error:{type: card_error|invalid_request_error|idempotency_error|rate_limit_error, code, decline_code, message, param, request_id}}`，客户端可以根据 `type` 判断是否应该重试。
- **版本管理**：采用日期版本 + 账户级 pin + 请求头显式覆盖三层机制；版本演进只允许新增字段，不允许删除或语义变更已有字段，保证旧版本客户端不会因为我们升级而突然出错。

## 1.5 状态机

PaymentIntent 的生命周期是整套设计的骨架，所有失败处理都要能映射回这个状态机上的某个节点：

```
requires_payment_method → requires_confirmation → requires_action(3DS 等强验证)
                                                 → processing → succeeded
                                                              ↘ requires_capture → succeeded
卡被拒绝（decline）→ 回到 requires_payment_method（允许换一张卡重试）
任一非终态 → canceled（释放已占用的授权额度；确认次数过多时可自动取消）
```

终态只有两个：`succeeded` 和 `canceled`；退款是另外一个独立对象 `refund(pending → succeeded|failed)`，不会让原 PaymentIntent 的终态发生倒退。`processing` 是一个特殊的"过渡态"——理想情况下它应该很快离开，但外部调用超时/未知结果时它可能会滞留，这也是第 5 节对账要重点监控的对象。

## 2. 数据模型

```
idempotency_keys(
  account_id, key, request_method, request_path,
  request_params_hash, locked_at, recovery_point,
  response_code, response_body, created_at
)
-- 唯一约束 (account_id, key)；这是整个幂等机制的真相源

payment_intents(
  id, account_id, amount, currency, status,
  payment_method_id, capture_method, latest_charge_id,
  last_error jsonb, created_at, updated_at, version
)
-- 可变业务对象；version 字段用于乐观锁防止并发更新冲突

charges(
  id, payment_intent_id, network_auth_code, network_txn_id,
  amount_captured, status, outcome jsonb, created_at
)
-- 每一次真正打到卡组织的授权/扣款留一条记录

ledger_entries(...)   -- 见 sd03 Ledger 题；这里只需要知道：授权成功后
                       -- 必须在同一套一致性保证下写入不可变的记账分录

outbox(id, aggregate_id, event_type, payload, published_at)
-- 状态变化通过 outbox 异步对外发通知（见 sd01 Webhook）
```

**分片键选择 `account_id`**：保证同一个商户的 PaymentIntent 与幂等键落在同一个分片内，让唯一约束能在单分片范围内高效生效，避免跨分片强一致的额外代价。

## 3. 一致性 / 幂等实现（核心）

这是这道题最容易被拉开分数的地方，用"先 claim 再外呼"的三段式流程：

```
T1（原子 claim）：
  INSERT INTO idempotency_keys(...) ON CONFLICT DO NOTHING
  - 插入成功 → 本次请求拥有该幂等键的处理权，recovery_point = started
  - 冲突且 recovery_point = finished → 直接返回缓存的 response_code/response_body
  - 冲突且 locked_at 很新（还在处理中）→ 返回 409，客户端可稍后重试
  - 冲突且 request_params_hash 不一致 → 返回 400 idempotency_error

T2（本地事务）：
  创建 payment_intent(status=processing)，recovery_point = pi_created
  （这一步和 T1 在同一个数据库里，可以用事务保证原子性）

外部调用（不在数据库事务内）：
  调卡组织发起授权；把我们自己生成的 charge_id 作为传给卡组织的幂等键，
  这样即便我们这边因为超时重试了这次外呼，卡组织那边也不会真的扣两次

T3（本地事务）：
  写 charges + ledger_entries + outbox；payment_intent.status = succeeded；
  recovery_point = finished；把最终响应写回 idempotency_keys.response_body
```

**崩溃恢复**：无论进程在哪个阶段崩溃，重试请求（或者一个专门的后台 completer 进程）都可以根据 `recovery_point` 知道接下来该做什么，而不是从头重新执行一遍——尤其是"外呼完成但 T3 还没落地"这个阶段崩溃时，恢复逻辑必须**先向卡组织查询该 charge_id 是否已经被授权**，再决定是继续走 T3 还是发起补偿（void 这笔未完成的授权），绝不能盲目地再发起一次新的外呼。这正是 Medium 作者 h7w 文章里指出的"senior 答不出、staff 才能答出"的关键点。

**Redis 的定位**：只作为已完成幂等键的快速读缓存（fast path），加速"同 key 重放直接返回缓存结果"这个高频场景；但 Redis 缓存丢失或不一致时，DB 唯一约束依然是能兜底保证正确性的真相源，绝不能让 Redis 成为判断"是否已处理"的唯一依据。

**过期清理**：幂等键设置一个较长的有效期（如 24 小时以上），过期后由后台 reaper 任务批量清理，避免存储无限增长；有效期内重放行为完全一致。

## 4. 失败处理

- **卡组织调用超时/连接中断**：这是最棘手的场景——我们自己都不知道钱扣没扣。正确动作是**先查询，再决定**：向卡组织发起幂等查询（用之前生成的 charge_id），确认这笔授权到底成功、失败还是仍未知；查询结果为"未知"时，把 payment_intent 标记为 `processing` 并交给后台对账任务持续跟进，绝不立即告诉商户"失败了"（否则商户可能引导用户重新支付，造成真实的重复扣款）。
- **部分失败（授权成功但记账失败）**：依赖 `recovery_point` 机制续写，绝不允许"先记账后授权"的顺序（那样会导致记账了但实际没扣到钱）。
- **并发操作同一个 PaymentIntent**：用乐观锁（`version` 字段）或对象级锁，冲突时返回 429（如 `lock_timeout`），客户端按约定自动退避重试。
- **区域故障 / 分区**：每个商户的写路径固定在一个 home region（单写者），跨区域只提供只读副本；发生故障需要切换 region 时，必须先 fence 掉旧的写路径，防止新旧 region 同时接受写入造成双写。
- **多步骤编排（风控 → 授权 → 记账 → 通知）**：用 saga 模式，每一步都有对应的补偿动作（例如 void 已经完成的授权），而不是依赖跨服务的分布式事务。

## 5. 对账 / 审计

- **每日对账**：拉取卡组织/收单行提供的结算文件，与我们自己的 `charges` 记录和 ledger 逐条核对；差异分成"可自动修复"（如金额取整误差）、"需要人工介入"、"暂时无法分类，下一周期再核"三类分别处理。
- **`processing` 滞留监控**：任何长时间停留在 `processing` 状态的 PaymentIntent（如超过 15 分钟）触发告警，这通常意味着外部调用结果未知，需要主动查询收尾。
- **审计要求**：记录保留周期要满足合规要求（通常以年为单位），所有涉及金额的状态变化都必须可追溯到具体的幂等键与请求。

## 6. 可观测性 + rollout

**监控指标**：授权成功率与拒绝率、p99 延迟、幂等冲突率（同 key 不同参数出现的频率，异常升高可能意味着客户端 bug）、`processing` 状态滞留数量、对账差异数量、卡组织错误率分布；全链路用 `request_id` 串联日志，方便一次请求从网关到卡组织再到记账的每一跳都能被追溯。

**rollout**：核心状态机的变更（比如新增一个中间状态）要先在影子流量或小比例商户上验证；任何涉及幂等键处理逻辑的改动都要格外谨慎，上线前用生产流量的镜像回放做验证，因为这里出 bug 的代价是真实的重复扣款或漏扣款；发布过程保留快速回滚开关。

## 7. 规模估算（简要）

假设峰值 1 万 TPS，每条请求/响应约 2KB，写入吞吐约 20MB/s；按合规要求留存多年，数据量会达到较大规模，需要分层存储（近期热数据在 OLTP，历史数据归档）。主要瓶颈在幂等键查找（DB 唯一索引 + Redis 前置缓存）与 ledger 的写入吞吐（按账户分片、必要时批量追加），以及下游 Webhook 通知的扇出压力。

## 8. 追问预演（面试中常见的几个连环追问）

- **"两个重试请求几乎同时打到不同实例，第一个还没写完幂等记录，第二个已经到了"**：这正是 T1 用数据库唯一约束做原子 claim 要解决的场景——无论两个请求打到哪个实例，`INSERT ... ON CONFLICT` 在数据库层面上是串行化的，只有一个能拿到"处理权"，另一个必然拿到冲突结果（要么是已完成的响应，要么是"处理中"提示），不存在两边都各自发起外部调用的可能。
- **"如果 Redis 缓存和 DB 出现不一致怎么办"**：以 DB 为准，Redis 只是加速已完成结果的读取；一次 Redis 缓存不一致最多导致多打一次 DB 查询（性能损失），不会导致重复扣款（正确性不受影响），这正是把 Redis 定位为"fast path 而非真相源"的意义所在。
- **"幂等键要保存多久，存储成本怎么控制"**：官方建议至少保留 24 小时以覆盖客户端的合理重试窗口；用后台 reaper 任务定期清理过期记录，控制存储增长；如果面试官追问"能不能更短"，可以讨论根据实际重试窗口的统计分布做动态调整。
- **"3DS 强验证怎么融入这个流程"**：授权过程中如果卡组织要求额外验证，PaymentIntent 进入 `requires_action` 状态，返回 `client_secret` 给前端完成用户交互验证，验证完成后前端再次调用 `confirm`（同样要求幂等键），流程回到主状态机继续往下走，不需要额外设计一套单独的重试逻辑。
- **"同一个用户在两台设备上几乎同时点了两次支付，这算不算幂等系统要解决的问题"**：不算——这是两个不同的业务意图（对应两个不同的 `Idempotency-Key`），幂等系统的职责是防止"同一个意图被重复处理"，而不是防止"用户产生了两个真实的支付意图"；后者属于产品/前端层面的防抖动或去重设计，超出这道题的核心边界，回答时明确划清这条线本身就是一个加分点。
