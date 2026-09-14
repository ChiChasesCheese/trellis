# 模型答案：短题三连（Connect 分账/Payouts · Feature Flag SDK · Metrics Counter Library）

> 取材：Stripe 文档 Payouts；Stripe 文档 Separate charges and transfers；`loop/raw/system_design.md` §4.6；培训站转述（feature flag、metrics 部分置信度 medium）。三道题各自独立按 `LOOP_GUIDE.md` §7 主线（视题目性质裁剪不适用的环节）组织，最后有一节讲三道题共通的时间管理策略。

---

# 第一题：Connect 分账与 Payout

## 0. 两句话复述 + 不变量

**复述**：平台代表第三方商户（连接账户）收款后，需要把资金按约定比例转给一个或多个连接账户，连接账户再定期把钱提现到银行；整个过程要保证资金移动是原子的（要么完全发生要么完全不发生），且不允许在没有足够可用余额的情况下透支提现。

**核心不变量**：转账是"一方扣、一方加"的原子操作，不多不少；`available` 余额才能被提现，`pending`（结算中）余额不能；每一笔余额变化都能追溯到具体的来源交易。

## 1. API 契约

```
POST /v1/transfers  Idempotency-Key
  {amount, currency, destination: acct_xxx, transfer_group?}
POST /v1/transfers/:id/reversals {amount?}
GET  /v1/balance → {available: [...], pending: [...]}
GET  /v1/balance_transactions?type=&payout=
POST /v1/payouts  Idempotency-Key  {amount, currency, method[standard|instant]}
POST /v1/payouts/:id/cancel
```

## 2. 数据模型

```
accounts(id, type[platform|connected|bank_clearing], country, default_currency, payout_schedule)
balances(account_id, currency, pending, available, version)   -- 物化，来源是账本（复用 sd03）
balance_transactions(id, account_id, type[charge|transfer|payout|refund|adjustment],
                      amount, fee, net, currency, available_on, status[pending|available], source_id)
transfers(id, source_account, destination_account, amount, currency, status, idempotency_key)
payouts(id, account_id, amount, currency, method, status[pending|in_transit|paid|failed|canceled],
        failure_code, bank_file_batch_id)
```

转账/提现的具体记账分录复用 sd03 已经建立的账本模型：转账 = `借 platform_available / 贷 connected_available`；提现 = `借 connected_available / 贷 bank_outgoing_clearing`，银行确认后再清空 clearing。

## 3. 转账原子性

- **同一分片内**：单个数据库事务，按账户 id 固定顺序加锁两个账户防止死锁，校验源账户 `available >= amount`，写两条账本分录并更新两条余额记录后提交。
- **跨分片/跨主体**：用 saga——源账户先"预留"（`available -= amount`，`held += amount`），目标账户入账成功后源账户再正式释放预留并终结整笔转账；任一步失败走补偿（释放预留）。全程用 `external_id` 幂等，每一步都可安全重放。

## 4. 失败处理

- **银行提现被退回**（可能延迟数天到达）：这是异步失败，写一条反向的 `balance_transaction` 恢复 `available` 余额，通过 Webhook（复用 sd01）通知商户，必要时暂停该账户的自动提现直到问题解决。
- **负余额**：退款/争议金额超过已入账余额时 `available` 会变成负数，触发一次 debit payout（从商户绑定的银行账户反向扣款）；如果反向扣款也失败，转入风控/挂账流程。
- **批处理 cut-off**：银行文件按国家/币种/通道分批生成，有明确的截止时间；每个 payout 只能进入一个批次（用 `bank_file_batch_id` 是否已设置来判断），批次重跑不会重复出款。

## 5. 对账

每日核对 Σ payouts.paid 是否等于银行对账单里的出款金额；每笔 charge 通过 `transfer_group` 关联的所有 transfers 之和不应超过该笔 charge 的净收入；pending→available 的翻转数量应与到期的 `balance_transactions` 数量一致。

## 6. 追问预演（分账/Payout）

- **"两个连接账户之间能不能直接互转，不经过平台账户？"**：产品设计上通常不允许（所有资金流动都要经过平台账户留痕，方便平台自己的对账与合规审查），如果业务上确实需要，也应该建模成"平台账户里两笔方向相反的记账分录同时发生"，而不是绕开平台账户直接在两个连接账户间转账。
- **"instant payout 和普通 payout 在设计上有什么不同？"**：instant payout 走实时的资金网络通道，失败/成功的反馈几乎是同步的，需要单独的限流（如每天次数上限）防止被滥用；普通 payout 走批处理的银行文件通道，失败反馈是异步且延迟的，需要更完善的重试/退回处理流程。

---

# 第二题：Feature Flag SDK

## 0. 两句话复述 + 不变量

**复述**：内部服务需要在不重新部署代码的前提下动态开关某个功能，支持按用户百分比灰度、按地区定向，并且能一键紧急关闭；这个判断会在每次请求里高频调用，延迟必须极低。

**核心不变量**：判定延迟必须是本地内存量级（不能每次判断都发一次网络请求）；配置中心不可用时，判定必须仍然返回一个确定的结果（fail-open 到预设默认值），不能让开关系统的故障变成业务请求的故障。

## 1. API（开发者怎么用）

```
SDK 侧（业务代码里调用，快路径）：
  is_enabled(flag_key: str, context: {user_id, region, ...}) → bool
  get_variant(flag_key: str, context) → str   # 支持多变体实验

管理侧（配置慢路径）：
  PUT /internal/flags/{key}
    {rules: [{type: percentage|region|user_list, value, rollout_pct}],
     default_value, kill_switch: bool}
```

`is_enabled` 是一个**纯本地计算**，不在请求路径上发起网络调用；`context` 里的字段（如 `user_id`）用一致性哈希映射到 0–100 的一个稳定值，用来实现"同一个用户在灰度百分比不变的情况下，判定结果始终稳定"（不会同一个用户这次刷到，下次又没刷到）。

## 2. 架构：慢路径 vs 快路径分离

- **慢路径（配置管理）**：规则存储在中心配置服务/数据库，管理界面/API 修改后触发一次配置版本更新。
- **快路径（判定执行）**：每个服务实例的 SDK 定期（如每隔几秒）或通过订阅推送拉取最新配置到本地内存，`is_enabled` 调用只读本地缓存，做哈希计算，不产生任何网络往返。

## 3. 失败处理

- **配置中心不可用**：SDK 继续使用**最近一次成功拉取的本地缓存**；如果服务刚启动、还从未成功拉取过，使用配置里预设的静态默认值（`default_value`），绝不因为拉取失败而抛异常阻塞业务请求。
- **紧急关闭（kill switch）**：设计成比常规灰度规则优先级更高的独立字段，一旦置位，判定逻辑直接短路返回"关闭"，不需要等待常规规则更新的完整发布流程，用于生产事故时快速止血。
- **配置更新的一致性**：不同服务实例拉取到新配置的时间点会有短暂差异（几秒到几十秒级别），这是可以接受的最终一致性，业务设计上不应该依赖"所有实例同一毫秒切换"这种强一致假设。

## 4. 可观测性 + rollout

判定结果本身要能被业务方低成本地打点上报（复用第三题的 metrics 能力），用来验证"灰度百分比是否符合预期""新功能打开后关键业务指标是否劣化"；新 flag 上线遵循先 0%（只记录不生效）→小比例→逐步放量的标准灰度节奏。

## 5. 追问预演（Feature Flag）

- **"两个不同的开关规则冲突了怎么办（比如既满足百分比灰度又命中了地区排除名单）？"**：规则之间要有明确的优先级顺序（比如 kill switch > 明确的用户/账户级覆盖 > 地区规则 > 百分比灰度 > 默认值），SDK 的判定逻辑按这个固定顺序依次求值，第一个命中的规则决定最终结果，避免"多条规则都命中、结果不确定"的歧义。
- **"要不要支持按账户而不是按用户做灰度？"**：`context` 结构本身设计成可扩展的键值对（不写死只支持 `user_id`），判定逻辑对不同维度的哈希/匹配方式是通用的，新增一种灰度维度不需要改动 SDK 核心逻辑，只需要新增一种规则类型。

---

# 第三题：Metrics Counter Library

## 0. 两句话复述 + 不变量

**复述**：分散在大量机器上的服务实例需要上报简单的数字型指标（计数、耗时分布、错误数），最终要能被聚合成统一的时间序列供查看趋势和设置告警；写入量远大于读取量，采集本身绝不能拖慢业务请求。

**核心不变量**：指标上报是**异步、非阻塞**的——业务请求的延迟不应该因为指标上报而增加；短期的少量指标丢失是可以接受的（不是财务数据，不需要 sd03 那种强一致保证）。

## 1. 架构：客户端本地聚合 + 服务端时间序列存储

- **客户端库（每个服务实例内嵌）**：提供 `counter.increment(name, tags)`、`histogram.record(name, value, tags)` 这类简单接口；库内部把同一个时间窗口（如 10 秒）内的相同指标在本地先聚合成一个数值（计数求和、耗时分布用近似的分桶直方图），再批量、异步地发送出去，而不是每一次业务调用都单独发一条网络请求——这是应对"写入量远大于读取量"的核心手段。
- **服务端聚合与存储**：接收各实例上报的预聚合数据，进一步按时间窗口和维度（tags）聚合成最终的时间序列，写入时间序列数据库；提供按名称+维度+时间范围查询的接口，供仪表盘和告警规则使用。

## 2. 数据模型

```
客户端本地：
  {metric_name, tags{...}, window_start, count, sum, min, max, histogram_buckets}

服务端存储（时间序列）：
  (metric_name, tags, timestamp) → {count, sum, p50, p90, p99, ...}
```

## 3. 失败处理与规模

- **上报失败/网络不通**：本地攒批的数据如果发送失败，允许在有限的内存缓冲里短暂重试，超过缓冲上限则直接丢弃最旧的数据而不是阻塞业务线程或无限占用内存——这是"少量指标丢失可接受"这条不变量的直接体现。
- **高基数问题**：如果某个维度（比如按用户 ID 打 tag）导致时间序列的组合数量爆炸，需要在客户端库层面就限制可用于打 tag 的维度种类，或者对高基数维度做采样/聚合降维，避免服务端存储被无限增长的序列数量压垮。
- **告警去抖**：短暂的指标抖动不应该立刻触发告警噪音，告警规则本身要有一定的时间窗口和阈值持续性要求（比如连续 3 个采样点超过阈值才告警），这是为了避免告警系统本身变成新的噪音源。

## 4. 可观测性 + rollout

系统自身的健康度也要被监控——比如客户端上报的丢失率、服务端聚合处理的延迟；新的指标接入或者聚合规则调整应该先在非关键的内部服务上验证，确认不会造成性能回退或存储成本失控后再推广。

## 5. 追问预演（Metrics）

- **"为什么不直接每次调用都发一条原始数据到服务端，让服务端统一聚合？"**：那样会让写入吞吐直接等于业务请求的吞吐，网络和服务端存储都会承受远高于必要的压力；客户端本地先做一层时间窗口聚合，能把发送频率降低几个数量级，这是应对"写入量远大于读取量"的关键设计决策。
- **"如果一个指标的 p99 耗时看起来异常高，怎么排查是不是聚合逻辑本身的问题？"**：分布式的近似直方图聚合（比如多个实例的分位数不能直接简单平均）本身有已知的精度折衷，回答里能主动提到"跨实例合并分位数需要用支持合并的近似算法（如 t-digest 类结构），而不是简单地对各实例的 p99 取平均"，是体现对这个领域细节理解的加分点。

---

# 三道题的共通点与时间管理

三道题看似领域不同，但都遵循同一个模式：**把"配置/规则怎么定"（慢路径，可以有一定延迟，重要的是灵活和可审计）与"运行时怎么执行判定/上报"（快路径，必须低延迟、非阻塞、能优雅降级）彻底分开**。这正是 Exponent 五维里"separation of concerns"这一维在三个不同场景下的统一体现，也是这一轮短题连问真正想考察的能力——识别出重复出现的设计模式，而不是把每道题都当成全新的问题从零想起。

**时间管理建议**：每道题控制在 8–10 分钟——先用 1 分钟点出核心矛盾，3–4 分钟给出 API/数据模型骨架，3–4 分钟讨论 1–2 个关键失败场景，留 1 分钟收尾。如果面试官在某一题上追问得比较深入，适度压缩后面题目的深度，但不要完全跳过任何一道，因为"能不能在时间压力下做优先级取舍"本身就是这个轮次在考察的能力之一。
