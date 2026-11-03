---
id: hi-pt-tt-wallet-ledger-service-7-hold-model
node: tt.sd.tt-wallet-ledger-service.points
type: qa
step: 6
---
## Q
**钱包与复式账本服务 · 冻结、确认、释放**｜必会 · 出自：钱包与复式账本服务 › 深入 3

钱包的冻结（hold）怎么设计？冻结 100 只确认 80 会怎样？要不要写分录？

## A
**要点。** 钱包行有 balance 和 held，可用额 = balance − held。冻结是 held + :c WHERE balance − held >= :c 加插入 Hold；确认用 UPDATE hold ... WHERE state='held' 影响 1 行才继续，balance 减确认额、held 减冻结额，余下 20 自动回可用额。
**竞争。** 确认与超时用同一条件，只有一个成功。
**分录。** 冻结只改 held 列：没改变谁拥有这笔钱，约 20% 不被确认，写分录是噪声；代价是靠 Hold 表还原历史冻结额。
