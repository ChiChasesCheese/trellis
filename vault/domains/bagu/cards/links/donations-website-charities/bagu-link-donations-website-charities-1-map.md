---
id: bagu-link-donations-website-charities-1-map
node: links.donations-website-charities
type: qa
step: 1
---
## Q
**限时捐款网站 · 会被追问哪些八股**｜必会

设计限时捐款网站时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 业务简单，难点全在和第三方付款服务打交道的不确定性。基础是：幂等与唯一约束、隔离级别下先查后插、间隙锁死锁、金额与时间存储、超时未知、隔离、对账。

**下钻路线。**
- 用户重复提交 → 前端防重加 Redis token 不够，最终落库唯一约束，[[a.idem.idempotency-design|幂等是什么、怎么实现]]
- 一人一次，先查后插为什么重复 → RR 快照读不等于当前读，唯一键兜底，[[a.mysql.isolation-levels|四个事务隔离级别与 ACID]]
- 先查再插偶发死锁 → 间隙锁阻塞插入意向锁，改唯一键直接插入，[[a.mysql.gap-deadlock|间隙锁、next-key 锁与死锁排查]]
- 金额和截止时间 → 金额用分或 DECIMAL，截止时间存 UTC，[[b.mysql.schema-money-backup|表设计规范]]
- 同一笔支付重试 → 客户端生成的幂等键传给 PSP，同键同体返回原结果，[[a.idem.payment-idempotency|支付与扣款接口的幂等设计]]
- PSP 超时到底扣没扣 → 未知状态，查询，同键重试，[[a.idem.timeout-unknown|调用扣款接口超时了，到底扣了没有]]
- 尖峰时线程堵在 PSP 调用 → 信号量限制并发调用数，[[b.protect.bulkhead|隔离]]
- PSP 与捐款表怎么核对 → 全量对账，差异逐条处理，[[a.idem.selection-reconciliation|分布式事务选型、最终一致与对账]]

**业务场景。** 用户点两次捐款，PSP 又超时、回调也丢了：幂等键保证不扣两次，对账把漏掉的那笔补回来。
**系统设计。** [[links.payment-batch-processing|支付处理系统（授权冻结 + 每日批量结算）]]：同样的超时未知与幂等，规模和批量结算更重；[[links.food-item-reviews|带打赏的菜品评价系统（点评 + 投票 + 达标付款）]]：同样需要付款恰好一次，触发条件是达标里程碑。
