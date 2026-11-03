---
id: hi-pt-tt-double-entry-ledger-10-test-cold
node: tt.lld.tt-double-entry-ledger.points
type: qa
step: 8
---
## Q
**复式账本（类设计） · 测试与日志增长**｜追问 · 出自：复式账本（类设计） › 取舍与追问

追问：怎么测试账本？日志无限增长怎么办？

## A
**测试。** 不平衡分录被拒；重复提交不改余额；冲正后余额回原值；多线程并发转账后各币种总和仍为 0 且 `verify` 为真；`balance_at` 边界序号。
**增长。** 按时间分区，旧分区转冷存储；余额索引和快照保证读取不依赖旧分区，审计需要时再读冷存储。
