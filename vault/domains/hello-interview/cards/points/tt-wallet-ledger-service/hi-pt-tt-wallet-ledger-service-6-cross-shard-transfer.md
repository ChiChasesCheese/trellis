---
id: hi-pt-tt-wallet-ledger-service-6-cross-shard-transfer
node: tt.sd.tt-wallet-ledger-service.points
type: qa
step: 7
---
## Q
**钱包与复式账本服务 · 跨分片转账**｜追问 · 出自：钱包与复式账本服务 › 深入 4

钱包转账双方在不同分片，不用分布式事务怎么保证不丢不重？

## A
**做法。** 转出方分片事务里借转出方、贷转账在途账户，以 transfer_id 为业务键，发件箱投递事件；转入方分片用同一个 transfer_id 幂等入账。
**状态机。** PENDING → DEBITED → CREDITED，或 DEBITED → REFUNDED。
**失败。** 转入失败（账户冻结或关闭）则回到转出方做反向分录补偿；任何一步用同一个键重放。
