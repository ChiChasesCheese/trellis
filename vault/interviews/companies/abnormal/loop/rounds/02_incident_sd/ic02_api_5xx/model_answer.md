# ic02 · 参考答案（portal-api 5xx + p99）

> 场景与全部数字均为 **(reconstructed)**：面经原话只有 "I was given access to an AWS environment and had to investigate an incident"（#8496901 Round 3），系统、根因、时间线是按 `tasks/AGENT_ONSITE.md` §3.B 构造的离线快照。
> 每条证据块的第一行是可原样运行的命令（在本目录），其后是输出里的原文行（`…` 表示省略）。`tests/test_ic02_model_answer.py` 逐块重跑并比对。

## 1. 一句话结论

两个阶段、一个根源。**阶段 A（09:40:07–09:52:14）**：`portal-api:88` 发布附带的迁移 `0142_alerts_timeline` 在一个事务里执行 `ALTER TABLE alerts ADD COLUMN` + 不带 `CONCURRENTLY` 的 `CREATE INDEX`，`ACCESS EXCLUSIVE` 锁持有 12 分钟；所有碰 `alerts` 的查询排队，占满 240 个池连接，其余请求等 10 s 拿不到连接 → 5xx ~70%。**阶段 B（09:52:14 起）**：流水线因 720 s 超时杀掉迁移，事务回滚，锁释放——但新端点 `/api/v2/users/{id}/timeline` 依赖的 `(tenant_id, user_id, created_at)` 索引也随之消失；该查询每次过滤掉 ~400 万行，把 RDS 读 IO 打到 gp3 上限、把连接池占满 → 5xx ~7.5%、平均 2 s。止血 = 关 flag `timeline_v2`；之后 `CREATE INDEX CONCURRENTLY`。

## 2. 时间线（UTC，2026-10-02）

| 时间 | 事件 | 证据 |
|---|---|---|
| 09:00–09:20 | `tn-orbit` 流量翻倍（放大器，无错误） | E14 |
| 09:33:10–09:35:40 | `portal-web` 部署：用户页开始调用 `/timeline`；老 API task 回 404 | E2、E15 |
| 09:37:50 / 09:38:20 | `ops-kim` 导入新证书并换到 ALB listener（无关） | E2、E13 |
| 09:39:30 | `portal-api:88` 滚动部署开始（flag `timeline_v2` 默认开） | E2、E3 |
| 09:40:05 / 09:40:07 | 流水线 `RunTask` 迁移；`BEGIN` → `ALTER TABLE` → `CREATE INDEX`（无 CONCURRENTLY） | E2、E4 |
| 09:40:09 起 | Postgres 日志：会话等待 `AccessShareLock on relation 16421`（= `alerts`），持锁 pid 40117 | E5 |
| 09:40:31–09:43:35 | 滚动期 15 个 task × 20 连接 > 可用槽位：`remaining connection slots are reserved` | E7 |
| 09:42 | 页面告警 `portal-api-5xx-rate-and-p99` 与 `rds-portal-prod-connections-high` ALARM | E0 |
| 09:44:10 | 部署 COMPLETED（健康检查 `/healthz` 不碰 DB） | E3 |
| 09:52:10 / 09:52:14 | 流水线 `StopTask`（720 s 超时）；Postgres `connection to client lost`，事务回滚，锁释放 | E4、E5 |
| 09:52 起 | top SQL 变成 timeline 查询；`ReadIOPS` ~11.8k；`Rows Removed by Filter` ~4M | E9、E10 |
| 09:57 | `rds-portal-prod-cpu-high` ALARM | E0 |
| 10:05 | 接手：5xx ~7.6%、平均响应 2.08 s、池 240/240 | E1、E7 |

## 3. 证据

### E0 · 在响的告警

```
$ python3 awsim.py alarms --table
2026-10-02T09:42:00Z  ALARM  portal-api-5xx-rate-and-p99  (AWS/ApplicationELB 5xxRatePct AND TargetResponseTime.p99 GreaterThanThreshold 5)
2026-10-02T09:42:00Z  ALARM  rds-portal-prod-connections-high  (AWS/RDS DatabaseConnections GreaterThanThreshold 270)
2026-10-02T09:57:00Z  ALARM  rds-portal-prod-cpu-high  (AWS/RDS CPUUtilization GreaterThanThreshold 80)
2026-10-02T09:39:00Z  OK     acm-portal-cert-days-to-expiry  (AWS/CertificateManager DaysToExpiry LessThanThreshold 14)
```

### E1 · 两个阶段（5 分钟粒度）

```
$ python3 awsim.py metrics get --namespace AWS/ApplicationELB --name RequestCount --stat Sum --start 09:30 --end 10:05 --period 300 --table
2026-10-02T09:30:00Z  86383.6
2026-10-02T09:45:00Z  95157.36
2026-10-02T10:00:00Z  93335.7
```

```
$ python3 awsim.py metrics get --namespace AWS/ApplicationELB --name HTTPCode_Target_5XX_Count --stat Sum --start 09:30 --end 10:05 --period 300 --table
2026-10-02T09:30:00Z  4.31
2026-10-02T09:45:00Z  66886.28
2026-10-02T10:00:00Z  6404.47
```

```
$ python3 awsim.py metrics get --namespace AWS/ApplicationELB --name HTTPCode_ELB_5XX_Count --stat Sum --start 09:30 --end 10:05 --period 300 --table
2026-10-02T09:30:00Z  0
2026-10-02T09:45:00Z  2786.75
2026-10-02T10:00:00Z  712.6
```

```
$ python3 awsim.py metrics get --namespace AWS/ApplicationELB --name TargetResponseTime --stat Average --start 09:30 --end 10:05 --period 300 --table
2026-10-02T09:30:00Z  0.05
2026-10-02T09:45:00Z  7.25
2026-10-02T09:50:00Z  4.39
2026-10-02T09:55:00Z  2.08
2026-10-02T10:00:00Z  2.08
```

```
$ python3 awsim.py metrics get --namespace AWS/ApplicationELB --name TargetResponseTime --stat p99 --start 09:30 --end 10:05 --period 300 --table
2026-10-02T09:35:00Z  0.3
2026-10-02T09:45:00Z  10.08
2026-10-02T10:00:00Z  10.07
```

5xx 率 = (Target 5XX + ELB 5XX) / RequestCount：09:30 档 0.005%，09:45 档 73.2%，10:00 档 7.6%。p99 两个阶段都钉在 ~10 s = 连接池 `pool_timeout`。

### E2 · 变更清单

```
$ python3 awsim.py trail lookup --start 09:30 --end 10:06 --table
2026-10-02T09:33:10Z  ecs.amazonaws.com  UpdateService  github-actions-deploy  {"cluster":"prod","service":"portal-web","taskDefinition":"portal-web:214"}
2026-10-02T09:37:50Z  acm.amazonaws.com  ImportCertificate  ops-kim  {"domainName":"portal.example.com"}
2026-10-02T09:39:30Z  ecs.amazonaws.com  UpdateService  github-actions-deploy  {"cluster":"prod","service":"portal-api","taskDefinition":"portal-api:88"}
2026-10-02T09:40:05Z  ecs.amazonaws.com  RunTask  github-actions-deploy  {"cluster":"prod","taskDefinition":"portal-api-migrate:88","startedBy":"deploy-pipeline/portal-api#2291"}
2026-10-02T09:52:10Z  ecs.amazonaws.com  StopTask  github-actions-deploy  {"cluster":"prod","task":"1958f81b4df6de960658e63ae0caa45f","reason":"Migration step exceeded 720s timeout (deploy-pipeline/portal-api#2291)"}
```

```
$ python3 awsim.py deploys --start 09:00 --table
2026-10-02T09:33:10Z  portal-web  portal-web:214  2026.10.02-0933-9a0c3e1  user page: show alert timeline (calls GET /api/v2/users/{id}/timeline)
2026-10-02T09:39:30Z  portal-api  portal-api:88  2026.10.02-0939-e7b05f1  add user alert timeline endpoint
2026-10-02T09:40:05Z  portal-api-migrate  portal-api-migrate:88  2026.10.02-0939-e7b05f1  add user alert timeline endpoint
```

### E3 · 新端点默认开启，依赖迁移建的索引

```
$ python3 awsim.py config diff portal-api --table
+ flags.timeline_v2: true
```

```
$ python3 awsim.py deploys --service portal-api --start 09:30
…
      "completedAt": "2026-10-02T09:44:10Z",
…
      "rollout": "ROLLING (min 100% / max 125%), health check GET /healthz (static, no DB)",
…
        "mode": "post-deploy-async",
        "timeoutSeconds": 720,
…
        "message": "add user alert timeline endpoint\n\nGET /api/v2/users/{id}/timeline behind flag timeline_v2 (default on).\nMigration 0142 adds an alerts(tenant_id, user_id, created_at) index for it."
```

### E4 · 迁移：一个事务、无 CONCURRENTLY、被杀、回滚

```
$ python3 awsim.py describe migrations 0142_alerts_timeline
  "transactional": true,
  "status": "ROLLED_BACK",
    "ALTER TABLE alerts ADD COLUMN triage_note_id bigint;",
    "CREATE INDEX alerts_tenant_user_created_idx ON alerts (tenant_id, user_id, created_at DESC);"
  "applied": false,
```

```
$ python3 awsim.py logs tail --group /ecs/portal-api-migrate --table
2026-10-02T09:40:07Z  migrate/1958f81b4df6de960658e63ae0caa45f  INFO  BEGIN
2026-10-02T09:40:07Z  migrate/1958f81b4df6de960658e63ae0caa45f  INFO  ALTER TABLE alerts ADD COLUMN triage_note_id bigint -- ok (4 ms)
2026-10-02T09:40:07Z  migrate/1958f81b4df6de960658e63ae0caa45f  INFO  CREATE INDEX alerts_tenant_user_created_idx ON alerts (tenant_id, user_id, created_at DESC)
2026-10-02T09:50:07Z  migrate/1958f81b4df6de960658e63ae0caa45f  INFO  still running: CREATE INDEX alerts_tenant_user_created_idx (elapsed 600s)
2026-10-02T09:52:10Z  migrate/1958f81b4df6de960658e63ae0caa45f  WARN  SIGTERM received: stopped by deploy pipeline (migration timeout 720s exceeded); closing connection
```

`ALTER ... ADD COLUMN`（无默认值）本身 4 ms，但它拿的 `ACCESS EXCLUSIVE` 锁**持有到事务结束**；同一事务里接着建 182M 行的索引，于是锁被持有了整整 12 分钟。

### E5 · 谁在等谁（Postgres 日志 + Performance Insights）

```
$ python3 awsim.py logs filter --group /aws/rds/instance/portal-prod/postgresql --pattern 'still waiting' --limit 2 --table
2026-10-02T09:40:09Z  portal-prod  LOG  process 41203 still waiting for AccessShareLock on relation 16421 of database 16401 after 1000.993 ms
```

```
$ python3 awsim.py describe pi portal-prod
      "AvgLoad": 270,
          "wait": "Lock:relation",
          "pid": 40117,
          "application_name": "portal-api-migrate",
          "lock": "AccessExclusiveLock on relation 16421",
          "blocked_sessions": 268
```

```
$ python3 awsim.py describe pg portal-prod.alerts
  "relation": "public.alerts",
  "oid": 16421,
  "n_live_tup": 182400000,
```

```
$ python3 awsim.py logs filter --group /aws/rds/instance/portal-prod/postgresql --pattern 'FATAL' --table
2026-10-02T09:52:14Z  portal-prod  FATAL  connection to client lost
```

```
$ python3 awsim.py logs filter --group /aws/rds/instance/portal-prod/postgresql --pattern 'acquired AccessShareLock' --table
2026-10-02T09:52:14Z  portal-prod  LOG  process 41879 acquired AccessShareLock on relation 16421 of database 16401 after 21877.402 ms
```

### E6 · 阶段 A 是"共享池耗尽"，不只是"表被锁"

```
$ python3 awsim.py logs insights --group /ecs/portal-api --query 'filter route = "/api/v2/users/{id}/risk" | stats sum(sample_rate) as requests by status' --start 09:42 --end 09:52 --table
status=500  requests=1100
status=503  requests=24200
```

```
$ python3 awsim.py logs insights --group /ecs/portal-api --query 'filter route = "/api/v2/config" | stats sum(sample_rate) as requests by status' --start 09:42 --end 09:52 --table
status=200  requests=18000
```

```
$ python3 awsim.py metrics get --namespace AWS/RDS --name CPUUtilization --start 09:30 --end 10:05 --period 300 --table
2026-10-02T09:35:00Z  17.46
2026-10-02T09:45:00Z  24.34
2026-10-02T10:00:00Z  90.94
```

```
$ python3 awsim.py metrics get --namespace AWS/RDS --name DBLoad --start 09:30 --end 10:05 --period 300 --table
2026-10-02T09:35:00Z  1.21
2026-10-02T09:45:00Z  269.97
2026-10-02T10:00:00Z  38.08
```

`/users/{id}/risk` 只读 `user_risk` 表，却全部 503：池里 240 个连接都在等 `alerts` 的锁（每个最多 30 s），它拿不到连接。`/config` 不碰数据库，全程正常。阶段 A 的 DB CPU 只有 ~25%、负载却 ~270 个会话（8 vCPU）：都在等锁。

按 Little 定律：240 个连接 ÷ 每个占 30 s = 每秒只有 ~8 个请求能拿到连接，并在 30 s 后被取消——ALB 15 s 先放弃，记为 504（E1：09:45 档 ELB 5XX 2,787 / 5 min ≈ 9.3/s）。

### E7 · 连接数：池与 max_connections 的账

```
$ python3 awsim.py metrics get --namespace AWS/RDS --name DatabaseConnections --stat Maximum --start 09:36 --end 10:05 --table
2026-10-02T09:39:00Z  159
2026-10-02T09:40:00Z  297
2026-10-02T09:44:00Z  293
2026-10-02T10:00:00Z  292
```

```
$ python3 awsim.py metrics get --namespace Portal/API --name DbPoolInUse --stat Maximum --start 09:55 --end 10:05 --period 300 --table
2026-10-02T09:55:00Z  240
2026-10-02T10:00:00Z  240
```

```
$ python3 awsim.py logs filter --group /aws/rds/instance/portal-prod/postgresql --pattern 'remaining connection slots' --limit 1 --table
2026-10-02T09:40:31Z  portal-prod  FATAL  remaining connection slots are reserved for non-replication superuser connections
```

```
$ python3 awsim.py config show portal-pg15-params
  "max_connections": 300,
  "superuser_reserved_connections": 3,
  "lock_timeout": 0,
```

300 − 3 = 297 个普通槽位；阶段 B 数据库连接 292、portal 池占用 240 → 其他客户端（alert-writer 等）约 52 个 → portal 可用 297 − 52 = 245。阶段 A 多出的 1 个（293）是迁移会话本身。12 task × 20 = 240 已贴边；滚动期 15 × 20 = 300 就撞墙。**所以"把池子调到 30"= 12 × 30 = 360，会让 alert-writer 等其他客户端也连不上。**

### E8 · 阶段 B：锁没了，什么还在耗数据库

```
$ python3 awsim.py metrics get --namespace AWS/RDS --name ReadIOPS --start 09:30 --end 10:05 --period 300 --table
2026-10-02T09:35:00Z  1428.63
2026-10-02T09:55:00Z  11818.95
2026-10-02T10:00:00Z  11776.13
```

```
$ python3 awsim.py describe rds portal-prod
      "StorageType": "gp3",
      "Iops": 12000,
```

```
$ python3 awsim.py describe pi portal-prod
          "wait": "IO:DataFileRead",
          "load": 27.9
          "sql": "SELECT id, kind, severity, created_at FROM alerts WHERE tenant_id = $1 AND user_id = $2 ORDER BY created_at DESC LIMIT 50",
          "load": 31.2
```

### E9 · 那条查询缺的正是被回滚的索引

```
$ python3 awsim.py logs filter --group /aws/rds/instance/portal-prod/postgresql --pattern 'Rows Removed' --limit 1 --table
2026-10-02T09:52:19Z  portal-prod  LOG  duration: 8539.853 ms  plan:
  ->  Index Scan Backward using alerts_tenant_created_idx on alerts  (cost=0.57..71662117.80 rows=3901 width=52) (actual rows=50 loops=1)
        Index Cond: (tenant_id = 'tn-orbit'::text)
        Rows Removed by Filter: 4025054
```

```
$ python3 awsim.py describe pg portal-prod.alerts
          "name": "alerts_tenant_created_idx",
          "def": "btree (tenant_id, created_at DESC)"
          "name": "alerts_tenant_status_created_idx",
          "def": "btree (tenant_id, status, created_at DESC, id DESC)"
          "tenant_id": "tn-orbit",
          "rows": 38100000
```

没有任何含 `user_id` 的索引：查询按 `tenant_id` 倒序走索引、逐行丢弃别的用户，为凑够 50 行读了 ~150 万个 buffer。

### E10 · 新端点：一成流量、三成错误、大租户最慢

```
$ python3 awsim.py logs insights --group /ecs/portal-api --query 'filter status >= 500 | stats sum(sample_rate) as requests by route' --start 09:55 --end 10:05 --table
route=/api/v2/alerts  requests=5000
route=/api/v2/alerts/{id}  requests=2400
route=/api/v2/users/{id}/risk  requests=2000
route=/api/v2/users/{id}/timeline  requests=4400
```

```
$ python3 awsim.py metrics get --namespace Portal/API --name RouteRequestCount --dim Route=timeline --stat Sum --start 09:55 --end 10:05 --period 300 --table
2026-10-02T09:55:00Z  10000.87
2026-10-02T10:00:00Z  10000.26
```

```
$ python3 awsim.py metrics get --namespace AWS/ApplicationELB --name RequestCount --stat Sum --start 09:55 --end 10:05 --period 300 --table
2026-10-02T09:55:00Z  93341.45
2026-10-02T10:00:00Z  93335.7
```

```
$ python3 awsim.py logs insights --group /ecs/portal-api --query 'filter route like "timeline" and status = 200 | stats pct(duration_ms, 50) as p50, count() as lines by tenant' --start 09:55 --end 10:05 --table
tenant=tn-kestrel  p50=2823.4  lines=21
tenant=tn-orbit  p50=8492  lines=17
```

09:55–10:05：timeline 20,001 次 / 全部 186,677 次（下一条命令）≈ 10.7%，但占 5xx 估计数的 4,400 / 13,800 ≈ 32%。`tn-orbit`（38.1M 行）timeline p50 8.5 s，其余租户 1.6–2.8 s。

### E11 · 应用不是瓶颈；扩容不会被触发（也不该）

```
$ python3 awsim.py metrics get --namespace AWS/ECS --name CPUUtilization --dim ServiceName=portal-api --start 09:30 --end 10:05 --period 300 --table
2026-10-02T09:35:00Z  33.35
2026-10-02T09:45:00Z  6.73
2026-10-02T10:00:00Z  15.24
```

```
$ python3 awsim.py describe ecs portal-api
      "healthCheck": "GET /healthz (static 200; does not touch the database)",
      "autoScaling": "target tracking on CPUUtilization 60%, min 12 max 24",
```

### E12 · 超时错位：应用记 500，ALB 记 504

```
$ python3 awsim.py logs insights --group /ecs/portal-api --query 'filter client_disconnected = 1 | stats sum(sample_rate) as n, min(duration_ms) as fastest by status' --start 09:55 --end 10:05 --table
status=500  n=1200  fastest=29849.9
```

```
$ python3 awsim.py describe elbv2 portal-alb
    "idle_timeout.timeout_seconds": "15"
```

ALB 15 s 就向客户端返回 504，应用里的查询还要跑到 30 s（`statement_timeout`）才被取消——白白占着连接和 IO。

### E13 · 红鲱鱼 1：证书轮换

```
$ python3 awsim.py config diff portal-alb --table
~ listener.certificateArn: "arn:aws:acm:us-east-1:111122223333:certificate/2f71c0a4-old" -> "arn:aws:acm:us-east-1:111122223333:certificate/9d03b6e8-new"
```

```
$ python3 awsim.py metrics get --namespace AWS/ApplicationELB --name ClientTLSNegotiationErrorCount --stat Maximum --start 08:30 --end 10:06 --period 3600 --table
2026-10-02T08:00:00Z  2
2026-10-02T09:00:00Z  2
2026-10-02T10:00:00Z  1
```

```
$ python3 awsim.py metrics get --namespace AWS/ApplicationELB --name HTTPCode_Target_5XX_Count --stat Sum --start 09:38 --end 09:40 --table
2026-10-02T09:38:00Z  0.84
2026-10-02T09:39:00Z  0.86
```

换证书后两分钟一切正常；TLS 握手错误全程 ≤ 2/min；错误类型是应用 503 与超时 504，不是握手失败。

### E14 · 红鲱鱼 2：`tn-orbit` 流量翻倍（放大器）

```
$ python3 awsim.py metrics get --namespace Portal/API --name TenantRequestCount --dim Tenant=tn-orbit --stat Sum --start 08:30 --end 09:40 --period 600 --table
2026-10-02T08:40:00Z  18046.07
2026-10-02T09:30:00Z  37769.91
```

```
$ python3 awsim.py logs insights --group /ecs/portal-api --query 'filter status >= 500 | stats count_distinct(tenant) as tenants' --start 09:55 --end 10:05 --table
tenants=9
```

09:20 起已是两倍流量，而 09:30 档 5 分钟内 Target 5XX 只有 4.31 次（E1）；现在 9 个租户都在出错。

### E15 · 旁支：09:35–09:43 的 404 是发布顺序

```
$ python3 awsim.py metrics get --namespace AWS/ApplicationELB --name HTTPCode_Target_4XX_Count --stat Sum --start 09:33 --end 09:45 --table
2026-10-02T09:34:00Z  50.38
2026-10-02T09:37:00Z  2087.03
2026-10-02T09:43:00Z  50.07
```

前端先上线并开始调用 `/timeline`，老 API task 回 404，新 task 滚动完毕即消失。与 5xx 无因果，但应进 postmortem（前端不应早于后端）。

## 4. 根因

- **触发**：迁移 `0142` 违反了大表迁移的两条规则——DDL 与建索引放进同一事务（锁持有到提交），以及建索引不用 `CONCURRENTLY`。迁移会话 `lock_timeout = 0`，它拿到锁后无限期持有，后面所有会话无限排队。
- **放大**：连接池满后所有端点共用的池被一个表的锁拖垮；`statement_timeout` 30 s > ALB 15 s，客户端早已放弃的查询继续占连接。
- **第二阶段**：流水线把超时迁移杀掉——锁问题自愈，但回滚了索引；发布流程没有"迁移成功"作为代码/flag 生效的前置条件，新端点在没有索引的情况下默认开启。
- **tn-orbit** 的 38M 行让缺索引的代价最大化，是放大器，不是原因。

## 5. 止血

1. **现在（10:05）**：关 `timeline_v2`。预期 1–2 分钟内 `RouteRequestCount{timeline}` → 0、`DbPoolInUse` < 40、`ReadIOPS` ~1.4k、5xx < 0.1%。
2. **之后（低峰）**：`SET lock_timeout = '3s'; CREATE INDEX CONCURRENTLY alerts_tenant_user_created_idx ON alerts (tenant_id, user_id, created_at DESC);`，确认 `pg_index.indisvalid`；失败则 `DROP INDEX CONCURRENTLY` 后重试。
3. **再之后**：按租户逐步开 flag（小租户先，`tn-orbit` 最后），盯 PI top SQL。
4. **不做**：提高池上限 / 扩 task（槽位只剩 ~5；09:40 已撞 `max_connections`）；单独限流 `tn-orbit`（治标）。
5. **如果是在阶段 A 接手**：`SELECT pg_terminate_backend(40117);` 立即释放锁（迁移回滚、稍后用正确方式重做）；比等 720 s 超时早 10 分钟恢复。
6. **沟通**：10:05 发 5 行状态（`investigation.md` §8），10:20 再更新；告知前端团队 timeline 暂时下线。

## 6. 长期修复

| 类别 | 行动 | 解决什么 |
|---|---|---|
| 迁移规范 | 索引一律 `CONCURRENTLY`（非事务）；DDL 单独、短事务；迁移会话 `lock_timeout` 3 s + 重试；带默认值/回填分三步（加列 → 分批回填 → 约束）；CI lint 拦截 | 阶段 A 不再发生 |
| 发布顺序 | expand → migrate 成功 → 部署代码 → 开 flag；迁移失败则阻断；前端晚于后端或 flag 门控 | 阶段 B 不再发生 |
| 超时一致 | 应用总超时 < ALB 15 s；按端点设 `statement_timeout`（读接口 5 s） | 放弃的请求不再占连接 |
| 容量 | 写下 `tasks × pool + 其他客户端 ≤ max_connections − reserved`；引入 RDS Proxy / PgBouncer；扩容策略检查连接预算 | 池与 DB 槽位的硬约束可见 |
| 舱壁 | 新 / 重端点独立小池；核心读路径保底 | 一个端点拖垮全站 |
| 告警 | 锁等待数、PI `Lock:*` 负载、`DbPoolWaitMs`、新出现的 top SQL；5xx 按 target/ELB 分开 | 发现时间从 2 分钟告警 → 定位时间更短 |
| 查询 | timeline 必须有 `(tenant_id, user_id, created_at)` 索引；大租户分页 + 时间窗；按租户限流 | 大租户放大效应 |

## 7. Postmortem 行动项

| # | 行动 | Owner | 优先级 |
|---|---|---|---|
| 1 | `CREATE INDEX CONCURRENTLY` 补索引，逐步重开 `timeline_v2` | portal-api owner | P0 |
| 2 | 迁移 lint + `lock_timeout` 默认值 + 禁止事务内建索引 | platform | P0 |
| 3 | 流水线：迁移成功才部署 / 开 flag；前端后于后端 | platform + portal-web | P1 |
| 4 | 超时梯度（应用 < ALB），读接口 `statement_timeout` 5 s | portal-api owner | P1 |
| 5 | 连接预算文档 + RDS Proxy 评估 + 按端点分池 | portal-api owner + DBA | P2 |
| 6 | 锁等待 / PI 告警；按租户限流 | on-call + portal-api owner | P2 |

## 8. 英文口播（90 s 总结）

> "There are two phases with one root. At 09:40 the portal-api 88 deploy ran migration 0142, which put an ALTER TABLE and a non-concurrent CREATE INDEX on the 182-million-row alerts table into a single transaction. The ALTER is instant, but its ACCESS EXCLUSIVE lock is held until the transaction ends, so for twelve minutes every query on alerts queued behind that session. Each queued query held one of our 240 pooled connections for up to 30 seconds, and everything else — even endpoints that never touch alerts — timed out after 10 seconds waiting for a connection: about 70% errors. At 09:52 the pipeline killed the migration after its 720-second timeout; the lock was released, but the rollback also removed the index that the new timeline endpoint relies on. Since then that query scans about four million rows per call for our largest tenant, read IOPS are pinned at the 12,000 provisioned, the pool is still full, and we're at about 7.5% errors and two-second averages. The certificate rotation and tn-orbit's doubled traffic are not causes: no TLS errors, and twenty clean minutes at double traffic. Mitigation: turn off timeline_v2 now — not raise the pool, we're 5 connections from max_connections — then build the index concurrently with a lock timeout and re-enable gradually. Long term: migration linting and lock timeouts, migrations gate the rollout, app timeouts below the ALB's, and a connection budget."
