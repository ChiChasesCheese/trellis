---
id: hi-c-sd-job-scheduler-b02-fencing
node: sd.problem-breakdowns.job-scheduler.beyond
type: qa
step: 2
---
## Q
**分布式任务调度器 · 拓展：租约过期后的"僵尸 worker"与围栏令牌**｜拓展 · 加分

worker A 因长时间垃圾回收暂停，租约过期后 B 接手并开始执行。A 醒来以为自己还持有租约，继续写结果。怎么挡住？

## A
- **问题：** 租约只能说明"在某个时刻我拥有"，不能保证"我现在仍然拥有"。暂停、网络延迟、时钟偏差都可能让持有者在失效后继续行动，造成重复执行或覆盖结果。
- **围栏令牌（fencing token）：** 每次发放租约都带一个单调递增的令牌；对共享资源的每次写操作都带上令牌，资源端只接受令牌不小于已见过的最大令牌的写。A 的令牌 1 已过时，B 的令牌 2 更新，A 的写被拒绝。
- **在数据库里：** `UPDATE ex SET status='DONE' WHERE id=? AND owner=? AND token=?`；影响行数为 0 说明自己已被取代。实测：A 取得令牌 1，租约过期后 B 取得令牌 2，A 尝试完成返回 False，B 完成返回 True。
- **局限：** 只有受令牌保护的写才安全；对外部副作用（已经发出的邮件）令牌拦不住，仍需要下游幂等。
- **为什么不依赖时钟：** 令牌是逻辑顺序，不受各机器时钟差异影响；租约时间只用于“什么时候允许别人接手”的判断，不用于判断“能不能写”。
- **模式。** 围栏令牌：用单调递增的版本号让资源端而不是持有者来判断谁有资格写。

```python
def finish(worker: str, token: int) -> bool:
    cur = db.execute("UPDATE ex SET status='DONE' WHERE id=1 AND owner=? AND token=?",
                     (worker, token))   # 令牌不是最新就更新不到任何行
    return cur.rowcount == 1
```
