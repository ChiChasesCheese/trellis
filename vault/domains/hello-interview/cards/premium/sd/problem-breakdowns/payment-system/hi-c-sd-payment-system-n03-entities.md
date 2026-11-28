---
id: hi-c-sd-payment-system-n03-entities
node: sd.problem-breakdowns.payment-system.notes
type: qa
step: 3
---
## Q
**支付系统 · 核心实体：PaymentIntent 与 Transaction**｜摘要 · 必会

支付系统为什么要把 PaymentIntent 和 Transaction 分开？两者是什么关系，生产环境里还会拆成什么？

## A
- **商户（Merchant）：** 使用平台的企业，含身份信息、银行账户、API 密钥。
- **PaymentIntent：** 商户想向顾客收取某笔金额的"意图"，跟踪整个收款生命周期，拥有状态机 created → authorized → captured / canceled / refunded，并负责幂等和重试。
- **Transaction：** 多态的资金流动记录，挂在一个 PaymentIntent 下，类型有 Charge（进账）、Refund（出账）、Dispute（可能的冲回）、Payout（给商户打款），含金额、币种、状态、时间戳，引用意图和商户。这里只关注 Charge。
- **关系：一对多。** 例：付款因余额不足失败，商户用同一个 PaymentIntent ID 重试，会生成新的 Transaction；分期付款对应多个 Transaction；退款是挂在原意图下的一条负金额 Transaction。
- **为什么分开：** 对商户来说只要创建一个意图，所有资金动作的复杂性由系统内部处理，提供简化的整体状态视图。
- **生产里更细：** 会拆成 Charge、Refund、Dispute、Payout 等独立类型，以及真正移动余额的复式记账分录（LedgerEntry）。面试里合并成一个多态 Transaction，足够讨论幂等、审计和故障处理。
