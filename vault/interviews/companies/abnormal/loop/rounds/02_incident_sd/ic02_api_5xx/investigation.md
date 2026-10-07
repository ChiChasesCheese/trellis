# ic02 · 推荐排查路径（portal-api 5xx + p99）

> 系统：ALB `portal-alb`（idle timeout 15 s）→ ECS `portal-api`（12 tasks，每 task 连接池 20、`pool_timeout` 10 s、`statement_timeout` 30 s）→ RDS Postgres `portal-prod`（`max_connections` 300）。前端 `portal-web` 是另一个服务。
> 本文讲**怎么走**；每一步的具体数字在 `model_answer.md`。所有命令在本目录运行。

## 0. 前 2 分钟：接班、定框

这是**交接**来的事故：已经持续 23 分钟，而且同事给了一条关键线索——"09:52 好了很多然后一直不好"。这句话意味着很可能有**两个阶段**，第一阶段的原因可能已经消失，第二阶段才是你现在要止血的。

先问 / 先说：

1. **影响面**：哪些用户、哪些页面？5xx 占比多少、慢多少？是所有租户还是某些租户？（portal 是安全分析师的工作台：慢 = 他们没法处置告警。）
2. **时间**：告警 09:42；同事说 09:52 有转折。要在图上找两个拐点。
3. **最近变更**：部署、迁移、配置、基础设施操作（CloudTrail）——这个时间段里很可能有不止一个。
4. **同事已经做了什么**：重启过吗？改过什么？（CloudTrail 里看得到 oncall-ana 只做了只读操作。）

> 🗣️ "Taking over: the alarm fired at 09:42 and my colleague says it improved at 09:52 but never recovered, so I'm expecting two phases — whatever started it may already be gone, and what's hurting customers right now may be something else. First: what's the error rate and latency now versus at peak, is it every tenant and every endpoint, and what changed between 09:30 and 09:52."

## 1. 量化现状：错误率、延迟、阶段

```
python3 awsim.py alarms --table
python3 awsim.py metrics get --namespace AWS/ApplicationELB --name RequestCount --stat Sum --start 09:30 --end 10:06 --period 300 --table
python3 awsim.py metrics get --namespace AWS/ApplicationELB --name HTTPCode_Target_5XX_Count --stat Sum --start 09:30 --end 10:06 --period 300 --table
python3 awsim.py metrics get --namespace AWS/ApplicationELB --name HTTPCode_ELB_5XX_Count --stat Sum --start 09:30 --end 10:06 --period 300 --table
python3 awsim.py metrics get --namespace AWS/ApplicationELB --name TargetResponseTime --stat Average --start 09:30 --end 10:06 --period 300 --table
```

要得出：09:40 起 5xx ~70%、平均响应 ~7 s；09:52 后降到 ~7.5%、~2 s，但没有回到基线（<0.01%、0.05 s）。**Target 5XX 是应用自己回的（503），ELB 5XX 是 ALB 等不及（504，15 s idle timeout）**——两个都要看。p99 两个阶段都卡在 ~10 s：这是一个"天花板"数字，10 s = 连接池的 `pool_timeout`，第一个线索指向连接池。

> 🗣️ "Two phases: 09:40 to 09:52 about 70% errors, after 09:52 about 7–8% errors and two-second average latency. p99 is pinned at ten seconds in both — that's exactly our pool checkout timeout, so I suspect connection-pool exhaustion and I'll look at the database next."

## 2. 变更清单（不急着下结论）

```
python3 awsim.py deploys --start 09:00 --table
python3 awsim.py trail lookup --start 09:30 --end 10:06 --table
python3 awsim.py config diff portal-api --table
python3 awsim.py config diff portal-alb --table
```

09:30–09:52 有五件事：`portal-web` 部署（09:33）、证书导入 + 换 listener 证书（09:37–09:38）、`portal-api:88` 部署（09:39:30）、迁移任务 `RunTask`（09:40:05）、迁移任务被流水线 `StopTask`（09:52:10，"exceeded 720s timeout"）。**StopTask 的时刻正好是同事说的转折点**。

> 🗣️ "Five changes in twenty minutes. The one that lines up with both inflections is the migration: it started at 09:40:05 and the pipeline killed it at 09:52:10. Let me see what it was doing."

## 3. 阶段 A（09:40–09:52）：锁

```
python3 awsim.py describe migrations 0142_alerts_timeline
python3 awsim.py logs tail --group /ecs/portal-api-migrate --table
python3 awsim.py logs filter --group /aws/rds/instance/portal-prod/postgresql --pattern 'still waiting' --limit 3 --table
python3 awsim.py describe pi portal-prod
python3 awsim.py describe pg portal-prod.alerts
python3 awsim.py metrics get --namespace Portal/API --name DbPoolInUse --stat Maximum --start 09:36 --end 09:46 --table
python3 awsim.py metrics get --namespace AWS/RDS --name DBLoad --start 09:30 --end 10:06 --period 300 --table
python3 awsim.py metrics get --namespace AWS/RDS --name CPUUtilization --start 09:30 --end 10:06 --period 300 --table
```

机制：迁移文件在**一个事务**里先 `ALTER TABLE alerts ADD COLUMN`（本身几毫秒，但拿了 `ACCESS EXCLUSIVE` 锁，**持有到事务结束**），再做不带 `CONCURRENTLY` 的 `CREATE INDEX`（182M 行，要十几分钟）。整段时间所有读写 `alerts` 的查询排队（Postgres 日志：`still waiting for AccessShareLock on relation 16421`，持锁 pid 40117；`describe pg` 说明 16421 就是 `alerts`）。每个排队的查询占着一个池连接 30 s（`statement_timeout`）→ 240 个连接全被占 → 其余请求等 10 s 拿不到连接 → 503。

两个容易漏的观察：
- RDS **CPU 很低**、DBLoad 却 ~270（8 vCPU）：会话都在等锁，不在干活。PI 的 top wait 是 `Lock:relation`。
- `users_risk` 路由根本不碰 `alerts`，也全挂了 → 是**共享连接池**被占满，不是表本身。

> 🗣️ "The migration wrapped an ALTER TABLE and a non-concurrent CREATE INDEX in one transaction. The ALTER is instant but its ACCESS EXCLUSIVE lock is held until commit, so for twelve minutes every query on alerts queued behind pid 40117. Each one held a pooled connection for up to 30 seconds, the pool of 240 filled, and everything else timed out after 10 seconds waiting for a connection — even endpoints that don't touch alerts. Load is 270 sessions on 8 vCPUs with CPU at 25%: they're waiting, not working."

（若你是在 09:45 接到 page：止血就是 `SELECT pg_terminate_backend(40117);`——事务回滚、锁立刻释放；代价是迁移要重做。流水线 12 分钟后替你做了同一件事。）

## 4. 阶段 B（09:52 之后）：为什么没恢复？

关键反问："锁已经没了，还剩什么在消耗数据库？"

```
python3 awsim.py metrics get --namespace AWS/RDS --name ReadIOPS --start 09:30 --end 10:06 --period 300 --table
python3 awsim.py describe rds portal-prod
python3 awsim.py logs insights --group /ecs/portal-api --query 'filter status >= 500 | stats sum(sample_rate) as requests by route' --start 09:55 --end 10:05 --table
python3 awsim.py metrics get --namespace Portal/API --name RouteRequestCount --dim Route=timeline --stat Sum --start 09:55 --end 10:05 --period 300 --table
python3 awsim.py logs insights --group /ecs/portal-api --query 'filter route like "timeline" and status = 200 | stats pct(duration_ms, 50) as p50, count() as lines by tenant' --start 09:55 --end 10:05 --table
python3 awsim.py logs filter --group /aws/rds/instance/portal-prod/postgresql --pattern 'Rows Removed' --limit 1 --table
```

PI 第三个窗口：top wait 变成 `IO:DataFileRead`，top SQL 是新端点 `/timeline` 的 `WHERE tenant_id = $1 AND user_id = $2 ORDER BY created_at DESC LIMIT 50`。`ReadIOPS` ~11.8k，贴着 gp3 预置的 12,000。auto_explain 显示它走 `alerts_tenant_created_idx` 倒序扫、`Rows Removed by Filter: ~4M`——因为**它需要的 `(tenant_id, user_id, created_at)` 索引就是那次被回滚的迁移要建的**。`describe pg` 确认表上没有含 `user_id` 的索引。

`/timeline` 只占 ~11% 的请求，却占 5xx 的 ~1/3；`tn-orbit`（38M 行）的 timeline p50 ~8.5 s，其他租户 ~2 s。它把 IO 打满、把池子占住，于是所有端点一起慢。

> 🗣️ "The lock is gone, but the rollback also took away the index the new timeline endpoint depends on. Performance Insights now shows IO waits, top SQL is the timeline query, and auto_explain shows it walking the tenant index backwards and discarding four million rows per call. Timeline is 11% of traffic but a third of the errors, and it's starving the pool for every other endpoint."

## 5. 红鲱鱼：用"还应该看到什么"排除

| 信号 | 如果它是原因，应当看到 | 实际 | 命令 |
|---|---|---|---|
| 09:38 换 ALB 证书 | TLS 握手错误上升；错误从 09:38 开始；是 ALB 层错误 | `ClientTLSNegotiationErrorCount` 全程 ≤ 2；09:38–09:40 两分钟 5xx 为 0；错误是 503（应用）和 504（超时） | `metrics get --namespace AWS/ApplicationELB --name ClientTLSNegotiationErrorCount ...`、`config diff portal-alb` |
| `tn-orbit` 流量翻倍 | 翻倍时（09:00–09:20）就出错；只有它出错 | 翻倍后 20 分钟 0 错误；09:55 后 9 个租户都有 5xx | `metrics get --namespace Portal/API --name TenantRequestCount --dim Tenant=tn-orbit ...`、`stats count_distinct(tenant)` |
| 09:35–09:43 的 4xx 突增 | — | `portal-web` 先上线，开始调用还不存在的 `/timeline`，老 task 回 404；`portal-api:88` 滚动完就消失。是部署顺序问题（值得写进 postmortem），不是这次 5xx 的原因 | `metrics get --namespace AWS/ApplicationELB --name HTTPCode_Target_4XX_Count ...` |
| 应用 CPU / 容量不够 | portal-api CPU 高 | CPU 从 ~33% **降**到 ~7–15%（在等数据库）；按 CPU 的 autoscaling 不会触发——幸好，扩容只会加连接 | `metrics get --namespace AWS/ECS --name CPUUtilization --dim ServiceName=portal-api ...` |

`tn-orbit` 是**放大器**：它最大（38M 行），timeline 查询最慢；但没有新端点 + 缺索引，它翻倍的流量什么事都没有。

## 6. 止血（现在是 10:05，处于阶段 B）

| 选项 | 效果 | 风险 / 取舍 |
|---|---|---|
| **关 feature flag `timeline_v2`**（推荐，第一步） | 秒级生效；去掉 top SQL；池子与 IO 立刻释放 | 新功能下线（前端要能优雅处理 404/disabled）；不影响老功能 |
| 回滚 `portal-api:87` | 同样去掉端点 | ~5 分钟滚动；连带回滚同一镜像里的其他改动；flag 更快更窄 |
| `CREATE INDEX CONCURRENTLY` 补索引 | 根治 | 182M 行在 IO 已打满时要很久；必须先关 flag 降压；并发建索引失败会留下 `INVALID` 索引要清理；设 `lock_timeout` |
| 提高池上限 / 扩 task | **更糟**：可用槽 297 − 52（其他客户端）= 245，现在已用 240；12 × 30 = 360 会撞 `max_connections`（09:40–09:43 已经出现 `remaining connection slots are reserved`），连 alert-writer 也会连不上；更多并发慢查询只会让 IO 更饱和 | 不做 |
| 对 `tn-orbit` 限流 | 减轻但不解决；还伤害最大客户 | 只在关 flag 不可行时考虑 |

验证（说出来）：`RouteRequestCount{timeline}` → 0；`DbPoolInUse` 回到 < 40；RDS `ReadIOPS` 回到 ~1.4k、CPU < 25%；5xx 回到 < 0.1%；p99 < 0.5 s。然后在低峰 `CREATE INDEX CONCURRENTLY`（带 `lock_timeout`），确认 `indisvalid`，再按租户逐步开 flag。

> 🗣️ "Mitigation now: turn off the timeline_v2 flag — it's the narrowest, fastest lever and removes the top query. I would not raise the pool size or scale out: we're at 240 of 245 usable connections and we already hit 'remaining connection slots are reserved' during the rollout. Once the database recovers, build the index with CREATE INDEX CONCURRENTLY and a lock_timeout, verify it's valid, and re-enable the flag gradually, starting with small tenants."

## 7. 长期修复

- **迁移规范**：DDL 与建索引分开，不放同一事务；大表索引一律 `CREATE INDEX CONCURRENTLY`（非事务）；迁移会话设 `lock_timeout`（如 3 s）+ 重试，拿不到锁就失败而不是排队把所有人堵住；加带默认值的列分三步（加可空列 → 分批回填 → 加约束）；CI 用 lint（如 squawk / strong_migrations 一类规则）拦截。
- **发布顺序**：expand → migrate（确认完成）→ 部署读新结构的代码 → 开 flag；流水线在迁移失败时**不应**让依赖它的代码继续生效。前端在后端之后上线（或用 flag 门控）。
- **超时一致性**：`statement_timeout`（30 s）> ALB idle timeout（15 s），客户端早走了查询还在跑；应让应用侧总超时 < ALB 超时，DB 侧按端点设更短的 `statement_timeout`。
- **容量模型**：tasks × pool + 其他客户端 ≤ max_connections − reserved；扩容策略要把它算进去；考虑 RDS Proxy / PgBouncer 做连接复用。
- **舱壁（bulkhead）**：按端点或优先级分池，新端点 / 慢端点不能拖垮核心读路径。
- **告警**：锁等待（`log_lock_waits` 已开，加指标）、`DBLoad` 中 Lock 类 wait、慢查询 / 新 top SQL、连接池等待；告警分 5xx 来源（target vs ELB）。
- **按租户限流**与查询成本保护（大租户的 timeline 分页 / 限时间窗）。

## 8. 5 行 incident summary（10:05 写给频道）

```
[MITIGATING] portal-api errors/latency — analysts see slow pages and ~7% errors (was ~70% 09:40–09:52)
Impact: 09:40–now UTC, all tenants; 09:40–09:52 ~70% of DB-backed requests failed; since 09:52 ~7.5% 5xx, avg 2 s.
Cause: migration 0142 held an ACCESS EXCLUSIVE lock on alerts for 12 min (ALTER + non-concurrent CREATE INDEX in one txn);
       it was killed and rolled back, so the new /timeline endpoint now runs without its index and saturates DB IO and the pool.
Mitigation: disabling flag timeline_v2 now; then CREATE INDEX CONCURRENTLY off-peak, re-enable gradually. Next update 10:20.
```

## 9. 自查清单

- [ ] 从交接话里听出"两个阶段"，并分别解释
- [ ] 区分 Target 5XX（应用 503）与 ELB 5XX（504），知道 10 s / 15 s / 30 s 三个超时各自对应什么
- [ ] 用 PI / 锁等待日志找到持锁 pid 与迁移；说清"ALTER 很快但锁持有到事务结束"
- [ ] 指出 `users_risk` 也挂 = 共享池耗尽，而非表锁直接影响
- [ ] 阶段 B 找到缺失索引与 top SQL，并联系到"迁移被回滚"
- [ ] 排除证书轮换与租户翻倍，并说出依据；把租户翻倍定性为放大器
- [ ] 止血选关 flag，并用连接数算术否定"加池子 / 扩容"
- [ ] 长期修复覆盖迁移规范、发布顺序、超时一致性、容量模型、舱壁、告警
