---
id: pay-correctness-webhooks-events-ordering-replay
node: correctness.webhooks-events
type: qa
step: 4
---
## Q
webhook 乱序到达时怎么处理？事件溯源和重放（replay）在修复事故时怎么用？

## A
**乱序**
- 状态机守卫：按状态阶位，过期事件忽略；允许跳过中间状态并补记。
- 事件版本：事件带创建时间或序号时，按它判断新旧，旧的不覆盖新的。
- 拉取确认（fetch-before-act）：收到事件后调 PSP 查询接口取对象的**当前**状态，以当前状态推进，而不是以事件内容推进。这样事件的顺序无关紧要。

**重放**
- 所有收到的事件完整保存（收件箱）。处理逻辑有 bug 时，修复代码后可以把受影响时间段的事件重新跑一遍。
- 前提：处理是幂等的，重放不会重复发货、重复记账；每个副作用都有幂等键。

**例子**：某次发布引入了 bug，3 天内 12 万条 `refund.succeeded` 事件被错误地丢弃为"未知类型"，导致退款单一直 pending。修复步骤：
1. 修代码并上线。
2. 查询收件箱：`event_type = refund.succeeded AND processed_at IS NULL AND received_at BETWEEN …`。
3. 把这些事件重置为未处理，由 worker 重新处理。
4. 每条处理都是幂等的：已经 succeeded 的退款单不会二次记账。
5. 对账验证：退款单状态与渠道退款文件一致。

**事件溯源的更强形态**：以事件序列作为状态的唯一来源，状态由事件重放得出。支付里更常见的折中是：当前状态加追加型状态历史加原始事件存档，足以审计和修复，复杂度可控。
