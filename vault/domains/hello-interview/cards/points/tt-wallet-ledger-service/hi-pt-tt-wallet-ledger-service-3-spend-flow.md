---
id: hi-pt-tt-wallet-ledger-service-3-spend-flow
node: tt.sd.tt-wallet-ledger-service.points
type: qa
step: 3
---
## Q
**钱包与复式账本服务 · 一次消费的事务流程**｜出自：钱包与复式账本服务 › 整体设计

钱包服务处理一次送礼消费，同步路径在分片库里怎么保证恰好一次、余额不为负、不要分布式事务？

## A
**步骤。** 同一本地事务：插入 Journal（business_key 唯一，冲突即处理过）；条件扣减 UPDATE wallet SET balance = balance - :p WHERE balance - held >= :p，影响行数 0 回滚返回 402；借用户账户、贷本分片 clearing 账户；写发件箱。
**为什么没有分布式事务。** 系统账户每个分片一份，一次业务的分录全在本片。
