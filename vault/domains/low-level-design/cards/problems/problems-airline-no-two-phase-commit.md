---
id: problems-airline-no-two-phase-commit
node: problems.booking.airline
type: qa
step: 5
tags: [grown]
---
## Q
航班管理设计里，跨航段的原子订座为什么不用两阶段提交或补偿事务（Saga），而是用固定顺序加锁？

## A
两阶段提交和 Saga 解决的是“库存分散在不同进程或机器上”的分布式一致性问题，这里所有 `FlightInstance` 都活在同一个进程里，`threading.Lock` 加固定的加锁顺序就能给出严格的原子性——按顺序拿到全部锁、在同一批锁里查完再写完。上分布式协议只会多一层这里根本不需要的复杂度；只有当库存真的跨机器时，才值得为这个问题换方案。
