---
id: hl-sd02-testing
node: system-design.sd02-job-scheduler
type: qa
step: 28
---
## Q
怎么确定性地测试调度器？

## A
- **虚拟时钟**：把时钟注入单写线程（`LongSupplier clock`），测试里手动 `advance(ms)`；时间轮 + 状态机是纯函数，测试毫秒级且无 `sleep`；
- **属性测试**：随机生成 (schedule, cancel, advance) 序列，断言：① 没有任务在 `fireAt` 之前触发；② 每个未取消任务恰好被触发一次（无故障时）；③ 触发延迟 ≤ tick；
- **崩溃重放测试**：在序列随机点「崩溃」（丢掉内存状态），用快照 + 日志恢复继续执行，最终触发集合必须与不崩溃的参考执行相同（至少一次下为超集且包含全部，去重后相等）；
- **故障注入**：leader 暂停（模拟 GC 停顿）后继续写，验证 fencing 拒绝；磁盘满；follower 落后；
- **差分测试**：与朴素的「排序 map」实现对照。
