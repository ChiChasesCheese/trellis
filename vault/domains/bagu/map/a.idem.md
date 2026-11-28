%% trellis:begin %%
# 幂等与分布式事务
*A 高频追问链*

幂等键、支付幂等、2PC / TCC / SAGA / outbox / 事务消息与对账。

## Topics
- [[domains/bagu/map/a.idem.idempotency-design|幂等是什么、怎么实现（Idempotency Keys, Unique Index, Token）]]
- [[domains/bagu/map/a.idem.payment-idempotency|支付与扣款接口的幂等设计（含支付回调）]]
- [[domains/bagu/map/a.idem.timeout-unknown|调用扣款接口超时了，到底扣了没有（Unknown Outcome）]]
- [[domains/bagu/map/a.idem.tcc|TCC：Try / Confirm / Cancel，空回滚与悬挂]]
- [[domains/bagu/map/a.idem.outbox|本地消息表 / Outbox 与最大努力通知]]
- [[domains/bagu/map/a.idem.selection-reconciliation|分布式事务选型、最终一致与对账（Reconciliation）]]
%% trellis:end %%

## Notes
