---
id: bagu-link-payment-batch-processing-1-map
node: links.payment-batch-processing
type: qa
step: 1
---
## Q
**支付处理系统（授权冻结 + 每日批量结算） · 会被追问哪些八股**｜必会

设计支付处理系统（授权冻结 + 每日批量结算）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 这套设计绕不开四个基础：重试不重复扣款（幂等），渠道超时是「结果未知」而不是失败，状态只能单向前进（状态机加条件更新），最后靠对账兜底。分片、金额精度和事件可靠通知是外围。

**下钻路线。**
- 开场：怎么保证重试不重复扣款 → 客户端生成幂等键，服务端对 (商户, 键) 建唯一约束，[[a.idem.payment-idempotency|支付与扣款接口的幂等设计]]
- 调用渠道超时 → 先落 PENDING 再调用，超时记 UNKNOWN，按引用号查询，查不到就冲正，不能换通道重发，[[a.idem.timeout-unknown|调用扣款接口超时了，到底扣了没有]]
- 授权冻结像哪种分布式事务 → TCC：冻结是 Try，请款是 Confirm，到期释放是 Cancel；状态机条件更新决定请款与到期谁赢，[[a.idem.tcc|TCC]]
- 支付成功怎么可靠通知账务 → 同事务写 outbox，中继至少一次投递，下游去重，[[a.idem.outbox|本地消息表 / Outbox 与最大努力通知]]
- 每秒一万笔按什么分片 → 按 holdId 哈希，冻结与请款同片，避免跨片事务，[[a.mysql.sharding|分库分表]]
- 每晚批处理主备切换，旧实例没停透 → 租约加围栏令牌，批次号做幂等键，[[b.distributed.fencing-token|Fencing Token、租约与脑裂防护]]
- 日终汇总差一分钱 → 全程用最小单位整数，分摊余数要有归属，[[b.runtime.java-money-bigdecimal|金额计算]]
- 卡号怎么不进我们的库 → 网关边缘换成令牌，真卡号只在隔离金库，日志只记字段白名单，[[b.scenario.card-tokenization-pci|卡号令牌化与 PCI 范围]]
- 商户请求怎么防伪造和重放 → HMAC 签名带时间戳，密钥放 KMS 并带编号轮换，[[b.scenario.request-signing-keys|请求签名与密钥轮换]]
- 账本怎么记 → 只追加的借贷分录，冲正追加反向分录，余额能由分录重算，[[b.scenario.ledger-design|复式账本]]
- 日终批量结算后怎么核对 → 账本、网络结算报告、银行到账三方比对，[[a.idem.selection-reconciliation|分布式事务选型、最终一致与对账]]

**业务场景。** 刷卡机上渠道超时，顾客换了一张卡再刷：旧那笔 UNKNOWN 冻结由后台冲正，否则同一笔消费在顾客账上冻了两次。
**系统设计。** [[links.tt-payment-reconciliation|支付对账系统（内部账本、PSP 结算文件、银行流水三方对账）]]：它接在日终结算之后，同一套幂等和未知状态，重心换成匹配规则；[[links.tt-merchant-webhook-delivery|商户回调（Webhook）投递系统（至少一次、重试、顺序、签名）]]：我们变成发送方，重试与去重的责任转给接收方。
