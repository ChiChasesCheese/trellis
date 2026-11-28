---
id: bagu-link-tt-payment-reconciliation-1-map
node: links.tt-payment-reconciliation
type: qa
step: 1
---
## Q
**支付对账系统（内部账本、PSP 结算文件、银行流水三方对账） · 会被追问哪些八股**｜必会

设计支付对账系统（内部账本、PSP 结算文件、银行流水三方对账）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 对账的数据量只有几 GB，难在口径对齐和时间差。依赖的基础是：固定时间点的快照读、唯一键让文件和匹配幂等、未知状态靠对账兜底、金额用整数、海量记录按分区排序后流式比对。

**下钻路线。**
- 为什么要三方 → 账本对 PSP 证明交易两边都有，PSP 批次对银行证明钱真的到了，[[a.idem.selection-reconciliation|分布式事务选型、最终一致与对账]]
- 千万笔怎么比对 → 按交易号分区、每片排序、双指针流式归并，不用子集和，[[b.scenario.massive-data-topk|海量数据]]
- 日终对账要前后一致 → RR 的 ReadView 固定在第一次读，RC 每次读都是新视图，[[a.mysql.mvcc|MVCC]]
- 两次读余额和明细对不上 → 不可重复读与幻读，对账读要固定时间点，长事务分批读，[[a.mysql.isolation-levels|四个事务隔离级别与 ACID]]
- 内外两边怎么对上同一笔 → 商户请求号同时是渠道引用号，一一对应，[[a.idem.payment-idempotency|支付与扣款接口的幂等设计]]
- 渠道不给查询接口 → 日终对账加人工队列，差异只追加调整分录，[[a.idem.timeout-unknown|调用扣款接口超时了，到底扣了没有]]
- 退款与批量对账偶发 1213 → 看 LATEST DETECTED DEADLOCK，统一加锁顺序，[[a.mysql.gap-deadlock|间隙锁、next-key 锁与死锁排查]]
- 账本和渠道账对不上时追到哪里 → 账本只追加，差额追到具体分录，调整只追加冲正分录，[[b.scenario.ledger-design|复式账本]]
- 对账文件和排查日志里有卡号吗 → 只用令牌和末四位，字段白名单，卡号格式扫描，[[b.scenario.card-tokenization-pci|卡号令牌化与 PCI 范围]]
- 金额口径不一致 → 统一成整数最小单位，币种带小数位数，永不用浮点，[[b.runtime.java-money-bigdecimal|金额计算]]

**业务场景。** 支付回调丢了一小时，渠道已扣款而订单仍是未支付：对账归为「账本缺失」，先向 PSP 查询确认，再补入账并通知订单继续履约。
**系统设计。** [[links.payment-batch-processing|支付处理系统（授权冻结 + 每日批量结算）]]：它是上游，批量结算完才轮到对账；[[links.tt-merchant-webhook-delivery|商户回调（Webhook）投递系统（至少一次、重试、顺序、签名）]]：回调丢失重复是「账本缺失」差异的主要来源。
