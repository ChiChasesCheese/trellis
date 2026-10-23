---
id: hl-j16-quiz-longadder
node: java21.j16-concurrency-primitives
type: qa
step: 41
---
## Q
`LongAdder` 为什么在高竞争下比 `AtomicLong` 快？代价是什么？什么时候不能用？

## A
- 快的原因：热点拆成 `base` + 多个 `Cell`，高竞争时不同线程更新不同 Cell（且 Cell 填充过，避免伪共享），避免同一内存位置的 CAS 重试和缓存行抖动。
- 代价：`sum()` 要遍历且**不是原子快照**，占更多内存。
- 不能用于需要**精确当前值参与决策**的场合：序号分配、限额 CAS 检查、达到阈值触发。
