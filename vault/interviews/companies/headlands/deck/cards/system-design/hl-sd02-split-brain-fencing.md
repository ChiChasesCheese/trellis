---
id: hl-sd02-split-brain-fencing
node: system-design.sd02-job-scheduler
type: qa
step: 23
---
## Q
旧 leader 发生 30 秒 GC 暂停后醒来仍自认 leader，会有什么危险？对策有哪四层？

## A
场景：leader A（epoch 7）暂停 30 s，协调服务租约过期、选出 B（epoch 8）开始分发；A 醒来仍继续分发 / 写日志，出现**两个 leader**。

对策（叠加使用）：
1. **epoch（fencing token）**：每次选主 epoch + 1，日志写入和对下游的交付都带 epoch，follower 与下游**拒绝旧 epoch**，A 醒来的第一次写就被拒；
2. **租约检查用单调时钟**：leader 每次分发前检查租约（`System.nanoTime()` 计时）是否有效，且 leader 租约时长**短于** follower 认为的时长（留时钟漂移余量）；
3. **幂等下游**：即使两个 leader 短暂都发了，同一 `jobId` 在下游只生效一次；fencing 减少重复，幂等保证正确，两道防线；
4. **Δ 预算**：故障切换 = 失败检测（租约 / 心跳超时 3–5 s）+ 选主（< 1 s）+ 热备追赶（≈ 0），所以第二档 SLO 取 10 s，宕机期间到期的任务在恢复后立刻按 fireAt 升序补发。
