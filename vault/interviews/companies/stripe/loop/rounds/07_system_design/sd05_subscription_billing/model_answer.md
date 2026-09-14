# 模型答案：设计订阅计费与发票系统（Subscription Billing & Invoicing）

> 取材：Stripe 文档《How subscriptions work》；`loop/raw/system_design.md` §4.5；复用 sd02（幂等支付）与 sd03（Ledger）的既有结论。按 `LOOP_GUIDE.md` §7 主线组织。

## 0. 两句话复述 + 不变量

**复述**：商户希望把自己的产品按周期（月/年）订阅的方式卖给用户，我们需要在每个计费周期自动生成账单并从用户的支付方式上扣款，同时支持试用期、按比例计费的升降级、扣款失败重试与最终的取消/暂停，全程不能因为系统重复执行某个任务而多开一张账单或多扣一次钱。

**核心不变量**：

1. **每个计费周期恰好一张正式发票**：不会因为调度器重跑或者并发处理而对同一个周期开出两张发票。
2. **每张发票恰好一次成功扣款**：扣款本身复用 sd02 的幂等支付 API，绝不双扣。
3. **三者状态最终一致**：订阅状态、发票状态、实际扣款结果三者不允许长期脱节（比如订阅显示 `active` 但已经连续几个周期扣款失败且没有任何后续动作）。
4. **金额计算可复现**：任何一笔比例计费/调整费用，事后都能根据订阅变更历史重新推导出当时是怎么算出来的。

明确不做什么：不追求"扣款瞬间"绝对精确到某一秒（错峰调度是有意为之的设计）；试用期结束、升降级生效的时间边界以我们系统记录的 UTC 时间为准，不承诺跨时区的"本地时间"精确对齐（本地时区只用于展示）。

## 1. 状态机

**订阅状态机**：

```
incomplete → active                （首张发票在规定时间窗内付清，如 23 小时内）
incomplete → incomplete_expired     （超时未付，发票作废）
trialing → active                   （试用期结束且有有效支付方式）
trialing → paused                   （试用期结束但没有可用的支付方式）
active → past_due                   （最新一张已生成的发票扣款失败或还未尝试）
past_due → active                   （补扣成功）
past_due → canceled | unpaid        （catch-up 重试用尽后，按商户设置的策略走其中一条）
unpaid → active                     （用户在到期前主动补齐）
任意状态 → canceled                  （终态；停止生成新发票、停止自动扣款）
```

**发票状态机**：

```
draft → open（finalize，即"定稿"，商户在定稿前有一个窗口可以追加调整项）
open → paid | void | uncollectible
```

两者的联动关系：一张发票的扣款结果会推动它所属订阅的状态往前走——`succeeded` 让订阅回到/保持 `active`；`card_error` 类失败让发票保持 `open` 同时订阅进入 `past_due`；需要用户强验证（如 3DS）时发票保持 `open`、订阅进入 `past_due` 直到用户完成验证。

## 2. API 契约

```
POST /v1/products, POST /v1/prices {unit_amount, currency, recurring: {interval, interval_count}}
POST /v1/subscriptions
  {customer, items: [{price, quantity}], trial_period_days?,
   collection_method[charge_automatically|send_invoice], proration_behavior}
POST /v1/subscriptions/:id
  {items?, proration_behavior[create_prorations|none|always_invoice], cancel_at_period_end?}
DELETE /v1/subscriptions/:id

GET  /v1/invoices/:id
POST /v1/invoices/:id/finalize
POST /v1/invoices/:id/pay
POST /v1/invoices/:id/void

所有写操作支持 Idempotency-Key（复用 sd02 的幂等机制）
```

契约细则：

- `proration_behavior` 让调用方明确表达"升降级时要不要按比例计费"，避免这个容易产生金额歧义的行为被隐式决定。
- `cancel_at_period_end` 与"立即取消"是两个不同的调用（前者只是打一个标记，订阅在当前周期结束后自然停止；后者立即终止并可能触发部分退款）。
- 发票有一个 `draft → finalize` 的窗口（如生成后 1 小时），给商户留出追加一次性费用条目的机会，之后才真正定稿并触发扣款。

## 3. 数据模型

```
subscriptions(
  id, customer_id, status, current_period_start, current_period_end,
  trial_end, cancel_at_period_end, default_payment_method,
  collection_method, latest_invoice_id, version
)

subscription_items(id, subscription_id, price_id, quantity)

invoices(
  id, customer_id, subscription_id, period_start, period_end,
  status[draft|open|paid|void|uncollectible],
  amount_due, amount_paid, attempt_count, next_payment_attempt,
  payment_intent_id, finalized_at, due_date
)
-- 唯一约束 (subscription_id, period_start)，这是防止重复开票的核心手段

invoice_line_items(
  id, invoice_id, price_id, quantity, amount,
  proration bool, period_start, period_end
)
-- proration=true 的行项目是升降级产生的比例调整费用

payment_attempts(id, invoice_id, payment_intent_id, attempted_at, outcome)
```

**时间统一用 UTC 存储**，本地时区只用于用户界面展示；日期不存在的边界情况（比如按月扣款但当月没有 31 号）统一取当月最后一天。

## 4. 核心流程

- **周期滚动**：调度器按时间分桶扫描 `current_period_end <= now` 的订阅（用带时间索引的队列而不是每次全表扫描，避免月初洪峰变成一次代价高昂的全表扫描）；对每个到期订阅，在一个事务内创建 `invoices(draft)` 并汇总当期的 `invoice_line_items`；给商户留一段窗口后 `finalize`；定稿后创建 PaymentIntent（幂等键绑定 `invoice_id`）发起扣款；结果通过 webhook（复用 sd01 的投递机制）通知商户，如 `invoice.paid` / `invoice.payment_failed`。
- **比例计费（proration）**：升级发生在周期中间时，计算"剩余周期内未使用的旧价退回"与"剩余周期内应补收的新价差额"两条调整行项目，公式为 `金额 × 剩余秒数 / 周期总秒数`，取整规则要固定并留痕（避免每次算出来的舍入结果不一致）；这两条调整项可以立即单独开一张发票，也可以并入下一期正式发票，取决于 `proration_behavior` 的配置。
- **扣款失败重试（dunning）**：按预设规则（如失败后 3 天、5 天、7 天再试）重试，每次尝试都写一条 `payment_attempts`；重试次数用尽后按商户配置决定订阅转为 `canceled`、`unpaid`，还是继续保持 `past_due` 观察；每次失败都应给用户发提醒更新支付方式的通知。
- **取消**：`cancel_at_period_end=true` 只是打标记，订阅继续正常运行到周期结束才停止；立即取消则作废尚未支付的发票，并可选按比例退还已经收取但未使用的部分（这一步的退款走 sd02/sd03 已经建立的支付与记账流程，不需要另起一套）。

## 5. 幂等与一致性

- **发票生成幂等**：`(subscription_id, period_start)` 唯一约束，调度器重跑或多个实例并发处理同一个订阅时，只会成功插入一条发票记录。
- **扣款幂等**：PaymentIntent 的幂等键由 `invoice_id + attempt_count` 组合而成，保证每一次重试尝试都是独立且安全可重放的，不会因为重试请求本身的重复投递而多扣一次。
- **订阅对象的并发更新**：用乐观锁（`version` 字段），例如用户同时在两个页面发起升级操作，只有一个能成功提交，另一个拿到冲突需要基于最新状态重新提交。
- **状态变化对外通知**：所有关键状态变化（发票创建/定稿/支付成功/支付失败、订阅状态变化）都通过 outbox 异步发出事件，复用 sd01 的 Webhook 投递设计，不在主流程里同步等待通知发送完成。

## 6. 失败处理

- **扣款结果未知**（比如调用超时）：复用 sd02 的"先查询、再决定"思路——不武断地把发票标记为失败或成功，而是标记为待确认，交给后台任务用查询接口确认真实结果后再推进状态机。
- **调度器自身故障**：处理任务本身要幂等（重复处理同一个订阅不会产生副作用），并且用"租约"机制（比如给正在处理的订阅打一个带过期时间的锁）防止多个调度器实例同时重复处理同一批订阅。
- **月初续费洪峰**：把"生成草稿发票"和"真正扣款"两个动作分开安排时间——提前一段时间批量生成草稿，把真正触发扣款的时间点错峰分散到一个更宽的时间窗口内，避免瞬时压垮下游的支付处理能力和 Webhook 通知系统；商户侧也被建议异步处理收到的 Webhook 通知，不要求同步实时响应。
- **时区/日期边界**：`current_period_end` 统一存 UTC；每月扣款日如果超出当月实际天数（如 31 号），按月末最后一天处理，这条规则要在文档里明确写出来，避免商户端产生"日期跳来跳去"的困惑。

## 7. 对账

每日批处理核对：Σ 已支付发票金额是否等于同期记入 ledger 的收入分录总额（复用 sd03 的账本设计）；扫描存在扣款记录但找不到对应发票的"孤儿 PaymentIntent"并报警；扫描长期停留在 `draft` 未定稿的发票，通常意味着调度或 finalize 环节出现了 bug 或积压。

## 8. 可观测性 + rollout

**监控指标**：续费成功率、催收（dunning）回收率、发票生成延迟、长期滞留的草稿发票数量、扣款状态处于"待确认"的滞留数量、Webhook 投递失败率。

**rollout**：任何计费规则（比如新的比例计费公式、新的重试节奏）上线前，先用历史订阅数据"模拟开票"（只计算不真正生成正式发票、不触发扣款），对比新旧规则计算结果的差异，确认没有意外的金额偏差后再灰度到小比例真实订阅；比例计费这类容易出金额错误的逻辑要有针对月份天数差异、周期正中间升级等边界情况的专门测试用例。

## 8.5 规模估算（简要）

假设平台有上亿活跃订阅、以月付为主，日常每天大约产生数百万张发票，月初可能达到平时的数倍甚至十倍；应对方式是把调度按时间分桶（避免所有到期订阅在同一时刻被处理）、`invoices` 表按 `customer_id` 分片、按月分区存储，扣款请求本身通过第 6 节的错峰策略平滑分散，避免瞬时峰值压垮下游的支付处理与 Webhook 通知系统。

## 9. 追问预演

- **"同一个周期为什么会开出两张发票，怎么排查？"**：先看是不是 `(subscription_id, period_start)` 的唯一约束被绕过了（比如某条代码路径直接插入而没有走统一的发票生成入口），这是这类 bug 最常见的根因。
- **"用户升级后立刻又降级回原套餐，中间的比例计费怎么处理？"**：每一次变更都独立生成对应的比例调整行项目并留痕，不会因为"结果上抵消了"就跳过记录——账本和发票的可追溯性要求过程透明，即便净结果是零。
- **"发票定稿后但还没扣款之前，客户改了支付方式，会用哪个支付方式扣款？"**：以订阅当前的 `default_payment_method`（或发票上单独绑定的支付方式，如果产品设计允许按发票覆盖）为准，实际发起扣款时才决定使用哪个支付方式，而不是在发票创建的那一刻就写死。
- **"试用期结束但用户一直没绑定支付方式，订阅会怎样？"**：进入 `trialing → paused` 而不是直接 `canceled`，给用户一个补充支付方式后继续订阅的机会；具体是暂停还是取消由商户在产品层面配置决定，系统本身要支持这种可配置的分支而不是写死一种行为。
- **"delayed 支付方式（比如银行转账类，确认要好几天）怎么融入这套状态机？"**：订阅可以先进入 `active`（Stripe 官方对这类支付方式的真实行为），发票保持 `open` 等待延迟到账的确认；如果最终扣款失败，走正常的 `invoice.payment_failed` 分支处理，订阅此时才转 `past_due`，而不是从一开始就让用户等待整个确认周期才能使用服务。

## 10. 与相邻题目的复用关系

这道题里"扣款"完全复用 sd02 的幂等支付 API 设计（幂等键、状态机、先查询再决定的失败处理）；"记账"完全复用 sd03 的双记账账本（每一笔发票收入、退款、比例调整都是账本上的具体分录组合）；"状态变化通知商户"完全复用 sd01 的 Webhook 投递设计。面试时能主动指出"这道题不是从零发明一套新机制，而是把前面几道题已经建立的机制组合应用到一个新的业务对象上"，是对整个 Stripe 领域体系融会贯通的直接证明。

## 11. 一句话总结

"订阅计费系统的骨架是一个按周期驱动的状态机，真正的难点不在于'定时扣一次钱'这个动作本身，而在于让发票生成、比例计费、扣款重试、订阅状态推进这几件事在任意组合的时序下都保持幂等和一致，并且不让月初的洪峰压垮下游系统。"

## 12. 常见误区小结（自查用）

- 误区一：把比例计费的舍入规则想当然地实现，不同代码路径用了不一致的取整方式，导致同一笔升级在报表里和在发票上金额对不上。
- 误区二：调度器扫描到期订阅时用简单的全表扫描 + `now()` 比较，没有考虑到分桶/索引优化，月初洪峰时直接拖垮数据库。
- 误区三：把"扣款失败"和"扣款结果未知"混为一谈，前者应该走 dunning 重试流程，后者应该先查询确认，两者处理不当都可能导致错误的双重扣款或长期挂起。
