---
id: pay-correctness-state-machines-states-transitions
node: correctness.state-machines
type: qa
step: 2
---
## Q
支付单、退款单、打款单各有哪些典型状态，哪些是终态？状态的"合法转移"具体是什么意思？

## A
**支付单**（payment）
- created → requires_action（需 3DS 等用户操作）→ authorized → captured
- 失败 / 终结分支：failed、voided（授权被撤销）、expired（超时未完成）、canceled
- captured 之后：partially_refunded、refunded（金额层面的派生状态）
- 终态：failed、voided、expired、canceled、refunded

**退款单**（refund）
- pending → succeeded / failed
- 终态：succeeded、failed

**打款单**（payout）
- created → submitted（提交渠道）→ paid；或 → failed；或 paid 后 → returned（银行几天后退回）
- 终态：failed、returned（paid 严格说也可被 return，所以 paid 在退票窗口内不算绝对终态）

**合法转移**：从状态 A 到状态 B 的一条允许的边。例如 `authorized → captured` 合法，`captured → authorized` 非法，`failed → captured` 非法。

**转移表**（集中定义）
- authorized：{captured, voided, expired}
- captured：{refunded（部分或全部）}
- 其他同理

**为什么重要**：非法转移意味着收到了不该出现的事件（乱序、重复或渠道异常）。系统要么忽略（幂等、已超前），要么报警进入人工，而不是直接写入。
