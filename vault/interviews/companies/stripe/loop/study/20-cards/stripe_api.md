# 卡片 · Stripe API 语义（Integration / System Design / Bug Squash 共用）

> 来源统一为 `loop/raw/stripe_official_and_api.md` §3（每条都摘自 docs.stripe.com，原采集 2026-09-01）。
> 本仓库的 `loop/mockserver/payments.py` 按这些语义实现了分页 / 429 / 幂等 / webhook 签名，可以对照着跑。
> 格式：`| Q | A | 出处 |`

## 幂等（idempotency）

| Q | A | 出处 |
|---|---|---|
| 幂等键保存的是什么？ | **第一次请求的状态码和响应体**，无论成功还是失败 | api/idempotent_requests |
| 同一个 key 重放一个当初返回 500 的请求，会拿到什么？ | **还是那个 500**。连错误都被完整重放，这是最常被追问的细节 | 同上 |
| 幂等键该怎么生成？ | V4 UUID 或等熵随机串；最长 255 字符；**不要用邮箱等敏感信息** | 同上 |
| 幂等记录保留多久？ | 至少 24 小时后可被清除。key 在被清掉之后重用 = 一个全新请求 | 同上 |
| 用同一个 key 但改了参数会怎样？ | 报错（`idempotency_error`）。幂等层会比对入参，不一致就拒绝 | 同上 |
| 哪两种情况**不会**落幂等记录？ | ① 入参校验就失败 ② 与另一个并发请求冲突（409）。这两种可以直接重试 | 同上 |
| 哪些请求需要幂等键？ | 所有 `POST`。`GET`/`DELETE` 天然幂等，不需要 | 同上 |
| 网络错误重试时，要不要沿用上次的 Idempotency-Key？ | **要**。这正是它存在的意义 | 同上 |
| 用户主动改了金额再提交，该用新 key 吗？ | **该**。否则触发 `idempotency_error` | 同上 |

## 错误模型

| Q | A | 出处 |
|---|---|---|
| 402 是什么意思？ | Request Failed：参数合法但请求本身失败（典型是卡被拒） | api/errors |
| 409 什么时候出现？ | 与另一个请求冲突，例如复用了同一个 idempotent key | 同上 |
| 424 是什么？ | External Dependency Failed：Stripe 的外部依赖挂了导致请求无法完成 | 同上 |
| 401 和 403 怎么区分？ | 401 = 没有有效 API key；403 = key 有效但没这个权限 | 同上 |

## 分页

| Q | A | 出处 |
|---|---|---|
| Stripe 用哪种分页？ | **游标分页**，参数是 `starting_after` / `ending_before` | api/pagination |
| `starting_after` 和 `ending_before` 能一起用吗？ | **不能，互斥** | 同上 |
| 两个游标参数接受什么值？ | 一个已存在的**对象 ID**（不是偏移量、不是时间戳） | 同上 |
| 列表返回的顺序是？ | **倒序时间**（reverse chronological） | 同上 |
| `limit` 的默认值和范围？ | 默认 10，范围 1–100 | 同上 |
| List 响应的固定结构？ | `{object: "list", url, has_more, data: [...]}` | 同上 |
| 怎么判断翻到底了？ | `has_more == false` | 同上 |
| 要拉全量数据的标准写法？ | 循环：读一页 → 若 `has_more` 则把**最后一个对象的 id** 传给下次的 `starting_after` | 同上 |
| 为什么面试答案是游标分页而不是 offset？ | offset 在数据频繁增删时会**跳过或重复**记录；游标天然稳定 | 同上 |
| v2 API 的分页跟 v1 一样吗？ | **不一样**，`/v2` 用另一套接口，不通用。版本迁移题常考 | 同上 |

## Webhook

| Q | A | 出处 |
|---|---|---|
| 签名放在哪个 header，什么格式？ | `Stripe-Signature`，格式 `t=<timestamp>,v1=<signature>` | docs/webhooks |
| 用什么算法签的？ | **HMAC-SHA256**，签的是 `f"{t}.{raw_body}"` | 同上 |
| 遇到非 `v1` 的 scheme 怎么办？ | **必须忽略**，防降级攻击。`v1` 是当前唯一合法 scheme | 同上 |
| 手动验签的四步？ | ① 拆出 `t` 和 `v1` ② 拼 `timestamp + "." + raw_body` ③ 用 endpoint secret 算 HMAC-SHA256 ④ **常数时间比较** + 查时间戳新鲜度 | 同上 |
| 为什么必须常数时间比较？ | 防时序攻击（用 `hmac.compare_digest`，不要用 `==`） | 同上 |
| 时间戳容忍度默认多少？ | **5 分钟** | 同上 |
| 容忍度能设成 0 吗？ | **不能**。官方明确警告：设 0 等于完全关掉新鲜度检查 | 同上 |
| 验签必须用什么 body？ | **原始 raw body**。任何改动都会导致验签失败——框架的 body-parser 中间件是最经典的坑 | 同上 |
| 生产环境重试多久？ | **最长三天，指数退避**（sandbox 是三小时内 3 次，跟生产不同） | 同上 |
| 事件顺序有保证吗？ | **没有**。官方举例：订阅创建可能产生 created → invoice.created → invoice.paid → charge.created，但顺序不保证 | 同上 |
| 能用 `created` 字段判断顺序或去重吗？ | **不能**。官方明确要求：**用 event ID 去重** | 同上 |
| 同一个业务动作对应了两个不同 Event 对象怎么去重？ | 用 `data.object` 的对象 ID + `event.type` 联合去重 | 同上 |
| handler 应该多快返回？ | 必须**先快速返回 2xx**，耗时逻辑丢异步队列 | 同上 |
| 除签名外还有什么防护？ | IP allowlist（Stripe 从固定 IP 段发） | 同上 |
| 轮换签名密钥时新旧能并存多久？ | 最多 24 小时 | 同上 |
| webhook 收到的对象能自动 expand 吗？ | **不能**。事件里的对象永远是最小形态，要展开得自己再发一次请求 | docs/expand |

## 限流（rate limits）

| Q | A | 出处 |
|---|---|---|
| 全局限流多少？ | Live **100 req/s**；Sandbox **25 req/s** | docs/rate-limits |
| 单个端点默认限流？ | **25 req/s**（除非另有说明） | 同上 |
| 429 会带什么 header 说明原因？ | `Stripe-Rate-Limited-Reason`，五种取值：`global-rate` / `endpoint-rate` / `global-concurrency` / `endpoint-concurrency` / `resource-specific` | 同上 |
| 速率限制和并发限制的区别？ | 速率限制通常**每秒重置**；并发限制统计**同一时刻有多少请求在处理中** | 同上 |
| 什么请求最容易撞并发限制？ | list 请求，以及带 `expand` 的请求（更耗资源、耗时更长） | 同上 |
| 处理 429 的标准做法？ | **指数退避 + 随机抖动（jitter）**，防雷鸣群效应；更高阶是客户端 token bucket | 同上 |
| 所有 429 都该无脑退避重试吗？ | **不是**。`code: lock_timeout` 的 429 是对象抢锁超时，不是限流；官方 SDK 会自动重试锁超时，但**不会**自动重试普通限流 429 | 同上 |
| 同一对象的并发写该怎么发？ | **串行排队**，不要并发发——否则撞 object lock timeout | 同上 |
| 读请求有额外配额吗？ | 有：平均每笔交易 500 次 GET（30 天滚动），每账户每月保底 10,000 次；写请求无此配额 | 同上 |

## Expand

| Q | A | 出处 |
|---|---|---|
| `expand` 解决什么问题？ | 把关联对象的 ID 换成完整对象，一次请求代替多次（省 N+1） | docs/expand |
| 展开的最大深度？ | **四层**：`property1.property2.property3.property4` | 同上 |
| 怎么展开列表里每个元素的属性？ | 用 `data` 关键字：`expand[]=data.payment_method` | 同上 |
| 是不是所有属性都能展开？ | 不是，文档里带 "Expandable" 标签的才行 | 同上 |
| 有属性是"不 expand 就拿不到"的吗？ | 有，例如 Checkout Session 的 `line_items` 默认不返回 | 同上 |
| expand 有什么代价？ | 拖慢请求；官方明确警告不要在 list 请求上做多层嵌套展开 | 同上 |

## 金额与货币

| Q | A | 出处 |
|---|---|---|
| API 里的金额怎么表示？ | 该货币**最小单位的整数**，不带小数点。`1000` = 10.00 USD，`10` = 10 JPY | docs/currencies |
| 零小数货币怎么处理？ | 如 JPY，金额数值直接相等，**不要乘 100** | 同上 |
| ISK / UGX 的坑？ | 规则上已是零小数货币，但为向后兼容**仍要求按两位小数传参**（收 5 ISK 传 `500`），且不能收零头 | 同上 |
| HUF / TWD 的坑？ | charge 按两位小数，但**手动 payout 必须传能被 100 整除的金额**——余额 HUF 10.45 时只能付出 `1000`，付不了全额 | 同上 |
| 为什么金额永远用整数不用浮点？ | 浮点累加会漂移，对账对不平。这是"设计货币字段"的标准答案 | 同上 |
| 卡组织的金额位数上限？ | 多数 12 位数字；**American Express 是 9 位**；日本境内 JCB/Diners/Discover 是 8 位 | 同上 |

## PaymentIntent 状态机

| Q | A | 出处 |
|---|---|---|
| 初始状态是什么？ | `requires_payment_method`（2019-02-11 之前的旧版叫 `requires_source`） | payments/paymentintents/lifecycle |
| `requires_confirmation` 常见吗？ | **大多数集成会跳过它**——提交支付方式和确认支付通常在同一步完成 | 同上 |
| 3D Secure 认证对应哪个状态？ | `requires_action`（旧版叫 `requires_source_action`） | 同上 |
| `processing` 什么时候进入？ | 完成必需操作后、且用的是**异步支付方式**（如银行代扣，可能几天） | 同上 |
| `requires_capture` 是独立大状态吗？ | 官方把它描述为 `processing` 的**分支路径**而非并列大状态——手动 capture 模式下先到这里 | 同上 |
| 支付被拒之后状态去哪？ | **退回 `requires_payment_method`** 以便重试。这是最常被漏掉的失败路径 | 同上 |
| 什么情况下会被系统自动 `canceled`？ | 被 confirm 的次数过多（官方的防暴力重试机制） | 同上 |
| 已经 `processing` 了还能取消吗？ | ACH / ACSS / AU BECS / BACS / NZ BECS / SEPA 这几种可以（有时间窗口，可能失败） | 同上 |

## 面试怎么用这些

| Q | A | 出处 |
|---|---|---|
| Integration 轮要"拉全量数据"，标准写法？ | `has_more` 循环 + `starting_after` 传上一页最后一个 id；配指数退避处理 429 | raw §3.3/3.5 |
| Integration 轮要"减少 API 调用"，标准答案？ | `expand`——但要主动说出它的两个代价（拖慢、webhook 里用不了） | raw §3.6 |
| System Design 轮设计"列表 API"，为什么选游标？ | offset 在频繁增删时跳记录/重记录 | raw §3.3 |
| webhook 题的四个必答追问是？ | 商户返 500 怎么办 · 商户 hang 住怎么办 · SSRF 怎么防 · exactly-once 能不能做到 | LOOP_GUIDE §7 |
| 一个 Staff 面试官对 webhook 题的真实拒因？ | "insufficient reasoning about failure modes and system abuse" | LOOP_GUIDE §7 |
| 本仓库哪里能真的跑这些语义？ | `loop/mockserver/payments.py`（分页 / 429+Retry-After / Idempotency-Key / Stripe-Signature 都实现了），`python3 loop/mock.py serve int02` | 本仓库 |
