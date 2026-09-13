# 模型答案：设计 Cron / Job Scheduler

> 取材：Blind IC1/IC2 一手报告（2025-07-03，"SQL engine as cron job"，面试官全程沉默）；PracHub "Reliable Job Scheduler"/"Cron Job Scheduler"；`catalog/raw/system_design.md` §1.4/§1.5。按 `LOOP_GUIDE.md` §6 主线组织。

## 0. 两句话复述 + 不变量

**复述**：这是一个把大量 SQL 查询当周期性任务管理的调度系统——用户注册一个 cron 规则，系统在分钟级精度下准确触发执行、记录结果、失败重试；调度器本身多实例部署，规模是百万量级任务，不能因为单个调度器实例挂了导致任务漏跑，也不能因为多实例同时抢同一个任务导致重复执行。

**核心不变量**：

1. **至少一次触发**：一个到点的任务必须被尝试执行，漏跑不可接受；重复触发在可控范围内可以接受（业务方需要能识别重复，但绝不接受"完全不跑"）。
2. **同一次触发的互斥执行**：同一个 `(job_id, scheduled_time)` 不能被两个调度器实例同时真正执行（会重复消耗执行引擎资源、产生重复的业务结果）。
3. **无状态可恢复**：调度器进程本身不持有权威状态，重启后完全依赖持久化存储决定下一步该做什么。
4. **故障隔离**：单个任务的失败/重试风暴不能影响其他任务的调度时效性。

明确"不做什么"：不追求秒级精度（题目明确分钟级）；不保证任务执行的 exactly-once（执行引擎本身可能重复执行，需要业务方或执行引擎层面幂等）。

## 1. API 契约

```
POST   /v1/jobs          {schedule: "cron或interval", task_ref, timezone, max_retries}
                          -> {job_id, next_run_at}
PATCH  /v1/jobs/:id       {pause|resume|update_schedule}
DELETE /v1/jobs/:id
GET    /v1/jobs/:id/runs?cursor=&limit=       # 每次触发的历史
POST   /v1/jobs/:id/trigger_now               # 手动立即触发一次（不影响下一次周期性调度）
```

- `schedule` 支持标准 cron 表达式或固定间隔（`every 15 minutes`），`timezone` 显式指定（cron 的日期计算依赖时区，DST 切换是常见 bug 来源，必须显式处理而不是假设 UTC）。
- `max_retries` 与失败退避策略在任务级可覆盖默认值。

## 2. 数据模型

```
jobs(
  job_id, schedule, timezone, task_ref, status[active|paused],
  next_run_at, max_retries, created_at
)
-- 索引 (status, next_run_at)：调度器扫描的核心查询
-- next_run_at 在注册时计算一次，每次触发完成后重新计算写回

job_runs(
  run_id, job_id, scheduled_time, status[pending|claimed|running|succeeded|failed|dead],
  owner_instance, lease_expires_at, attempt_count, started_at, finished_at, error
)
-- 每次触发一行；(job_id, scheduled_time) 唯一约束防止重复生成触发记录
-- 索引 (status, lease_expires_at) 供 worker 扫描可执行/可抢占的 run

shard_leases(
  shard_id, owner_instance, lease_expires_at
)
-- 调度器实例的分片租约表，心跳续租
```

## 3. 核心流程

**任务注册**：计算 `next_run_at`（cron 表达式在给定时区下的下一次触发时间），写入 `jobs`。

**分片与扫描**：`job_id` 按哈希分成 N 个逻辑分片；每个调度器实例通过 `shard_leases` 表用条件更新（`UPDATE shard_leases SET owner=me, lease_expires_at=now()+30s WHERE shard_id=X AND (owner IS NULL OR lease_expires_at < now())`）抢占若干分片并定期续租；每个实例只在自己持有租约的分片范围内，周期性（如每 30 秒）扫描 `jobs WHERE status=active AND next_run_at <= now()`。

**触发/派发**：扫到到点任务后，先向 `job_runs` 插入一条 `(job_id, scheduled_time, status=pending)`（唯一约束保证同一触发时刻只会有一行，即便多个实例并发扫描到也只有一个能插入成功）；然后用条件更新把这一行原子地"认领"为自己（`status=pending -> claimed, owner_instance=me, lease_expires_at=now()+N`）；认领成功才真正调用执行引擎跑对应的 SQL，`status -> running`；执行结束更新为 `succeeded`/`failed`，同时把 `jobs.next_run_at` 重新计算写回。

**互斥的关键**：不是"大家商量好谁来跑"，而是**数据库的唯一约束 + 条件更新（compare-and-swap）是真相源**——即使分片租约出现短暂的双持有（网络抖动导致两个实例都认为自己持有同一分片），最终真正认领 `job_run` 这一步的条件更新也只会有一个实例成功，另一个会更新失败并放弃执行。

## 4. 失败模式与规模

**崩溃恢复**：调度器实例本身不维护"接下来该跑什么"的内存队列，每一轮扫描都是从数据库重新查询当前到点且未被认领的 job_run；实例崩溃重启后，之前它持有的分片租约会在 30 秒后过期，被别的存活实例接管，接管后扫描到的仍然是数据库里的权威状态——不会因为进程重启而"忘记"要跑什么，也不会因为不知道之前跑到哪而重复补跑所有历史（`(job_id, scheduled_time)` 唯一约束已经保证了同一触发时刻不会被重复插入 job_run）。

**Lease 超时后的重新认领**：如果一个 worker 认领了 job_run 之后自己挂了（没有更新为 succeeded/failed），`lease_expires_at` 到期后，其他 worker 的扫描逻辑会把这类"claimed/running 但 lease 已过期"的 run 重新纳入可认领范围，重新执行——这是"至少一次"语义的来源，代价是这种场景下会重复执行一次（业务方需要能接受或自己做幂等）。

**失败重试与隔离**：单次执行失败按指数退避重新调度（如 1min → 5min → 30min），达到 `max_retries` 后转入 `dead` 状态并告警，不再自动重试（类比 Snowflake Tasks 的 `SUSPEND_TASK_AFTER_NUM_FAILURES`），防止一个持续失败的任务反复被扫描、反复占用执行资源，拖累其他健康任务的调度时效性。

**规模估算**：1e6 任务、分钟级精度，意味着调度器整体每分钟大约要检查 1e6 行里 `next_run_at <= now()` 的子集——只要索引 `(status, next_run_at)` 命中，这是一个范围扫描而不是全表扫描，代价可控；按 N 个分片水平拆开后，单实例只需要处理 1e6/N 量级的任务，可以线性扩容；执行层（真正调用执行引擎的 worker）与调度/扫描层解耦、独立扩容，避免"执行慢"拖慢"发现该跑什么"这一步。

**多副本 lease 的正确性边界**：租约机制本身依赖"lease_expires_at 到期"这个判断，如果机器之间时钟不同步会有边界问题——用相对宽松的租约时长（远大于典型的时钟漂移量）和单调时钟（而不是挂钟）做续租判断可以缓解，但无法完全消除"极端情况下短暂双持有"的可能性，这也是为什么最终互斥要靠数据库条件更新兜底，而不是单纯信任 lease。

## 5. 分层与组件

- **调度计算层**：cron 表达式 → next_run_at 的纯函数，注册和每次触发完成后调用，不掺杂在扫描循环里，便于独立测试（包括 DST 切换等边界情况）。
- **分片协调层**：`shard_leases` 表 + 心跳续租，只负责"谁负责扫哪些 job_id"，与真正的任务执行逻辑无关。
- **扫描/触发层**：无状态，定期扫描自己负责分片内到点的任务，做认领（CAS）。
- **执行层**：真正调用执行引擎的 worker 池，与扫描层通过 `job_runs` 表解耦，可独立扩容。

## 6. rollout/测试/监控

- **监控**：调度延迟（`实际触发时间 - scheduled_time` 的 p50/p99）；失败率与 dead 任务增长率；分片再平衡频率（频繁再平衡说明实例不稳定）；单实例负载（每分片任务数 × 扫描频率）。
- **测试**：把系统时钟往前拨的集成测试验证跨 DST、跨月边界的 cron 计算正确；故障注入测试验证租约过期后的重新认领不会重复执行超出预期次数。
- **rollout**：新的调度/分片算法先跑影子模式（只记录"这一轮我会触发哪些任务"但不真正派发）对比新旧逻辑差异，确认没有系统性漏跑或重复后再切流量；告警覆盖"某分片长期无人认领"（所有实例都不健康）这种全局性故障。

## 7. 用 Snowflake 自己的原语作参照

这道题几乎就是 Snowflake 自己的 **Tasks** 产品的简化面试版（`01-company-brief.md` §1）：Tasks 支持 CRON 或固定间隔调度、可以组成 DAG、用 `WHEN SYSTEM$STREAM_HAS_DATA()` 避免空跑、可以跑在 serverless 或用户自管的 warehouse 上、`SUSPEND_TASK_AFTER_NUM_FAILURES` 在连续失败后自动挂起任务、`TASK_HISTORY()` 提供每次运行的历史记录——这与本题设计里的 `jobs`/`job_runs` 表、失败自动暂停、运行历史查询几乎一一对应。面试时可以直接说："这本质上是在重新设计 Snowflake 自己的 Tasks 调度器，`job_runs` 表就是简化版的 `TASK_HISTORY`，failure 隔离对应的就是 `SUSPEND_TASK_AFTER_NUM_FAILURES`。"这既展示了对 Snowflake 产品的理解，也证明了设计的合理性有真实生产系统背书。

## 8. 45 分钟口述时间表

- **0–5 min**：复述题目 + 不变量（at-least-once 触发、互斥执行、无状态可恢复、失败隔离），确认 1e6 规模与分钟级精度、cron 时区处理。
- **5–12 min**：API 契约（注册/暂停/手动触发）+ 数据模型（jobs / job_runs / shard_leases 三张表）。
- **12–22 min**：核心流程——分片扫描、CAS 认领、执行、失败重试与 next_run_at 重算。
- **22–35 min**：失败模式——崩溃恢复为什么不丢不重复（唯一约束 + CAS 是真相源）、lease 超时后的重新认领、失败隔离（自动暂停）、规模估算。
- **35–42 min**：分层图 + rollout（影子模式验证新调度逻辑）+ 监控指标。
- **42–45 min**：总结 + 主动提出"这本质是在重造 Snowflake Tasks"，反问面试官。
