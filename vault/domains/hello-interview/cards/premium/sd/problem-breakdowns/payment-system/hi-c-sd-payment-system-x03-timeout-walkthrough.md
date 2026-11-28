---
id: hi-c-sd-payment-system-x03-timeout-walkthrough
node: sd.problem-breakdowns.payment-system.exam
type: qa
step: 3
---
## Q
**支付系统 · 推演：200 美元的扣款超时**｜考点 · 必会

向银行发 200 美元扣款，30 秒无响应。写出各个时刻的状态、该对商户说什么，商户用同一个幂等键重试会发生什么，银行后来说"已扣款"又怎么处理？

## A
- **发起前：** 先写尝试记录（网络、引用号、金额），状态 `initiated`，触发 CDC 事件。
- **30 秒超时：** 尝试更新为 `timeout`，PaymentIntent 为 `processing` 或 `pending_verification`，不是 `failed`。
- **对商户：** 返回"处理中，结果待确认"，不要说失败；建议商户等待状态变化或 Webhook，不要让顾客换卡重付。
- **商户用同一个幂等键重试：** `(商户ID, 幂等键)` 唯一约束命中，返回已有记录的当前状态（仍为处理中），而不是再发一次扣款。
- **对账服务：** 用引用号查询银行。银行答复"已扣款"：尝试改为 `succeeded`，意图改为 `succeeded`，CDC 事件触发 Webhook 通知商户。答复"无此交易"：标 `failed`，允许新的支付尝试。查询也超时：保持待核实，按退避再试；最终以网络的结算文件为准。
- **关键：** 状态只在得到权威信息后才进入终态；整个过程每步都是事件，可审计。
