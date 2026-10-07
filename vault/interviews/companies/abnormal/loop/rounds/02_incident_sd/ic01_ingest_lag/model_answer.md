# ic01 · 参考答案（alert-ingest consumer lag）

> 场景与全部数字均为 **(reconstructed)**：面经原话只有 "I was given access to an AWS environment and had to investigate an incident"（#8496901 Round 3），系统、根因、时间线是按 `tasks/AGENT_ONSITE.md` §3.B 构造的离线快照。
> 每条证据块的第一行是可原样运行的命令（在本目录），其后是输出里的原文行（`…` 表示省略）。`tests/test_ic01_model_answer.py` 逐块重跑并比对，所以这里的数字与快照一致。

## 1. 一句话结论

14:02 的部署 `alert-ingest:57`（"simplify geoip client"）把 geo-ip 查询从"批量 + 本地 LRU 缓存 + 带抖动退避"改成"每条消息一次同步调用、零退避重试"；请求量从 ~20/min 涨到 ~3,200/min，被 `geoip-svc` 的 per-client 限额 1,200 rpm 拒掉六成以上（429），成功查询被钉在 20/s，而生产是 ~150/s → 消费速率从 ~160/s 掉到 ~22/s，lag 每分钟 +~7,800 线性增长，约一成消息耗尽 5 次重试进 DLQ。止血 = 回滚到 `alert-ingest:56`；扩容无效。

## 2. 时间线（UTC，2026-09-30）

| 时间 | 事件 | 证据 |
|---|---|---|
| 12:55 → 13:01 | MSK broker-2 磁盘告警 ALARM → OK（ops 扩容 1000→1500 GiB）；lag 无变化 | E10 |
| 13:58:41 | `report-renderer` 部署到 `prod-batch` 集群（与本事故无关） | E3、E11 |
| 14:01:48 / 14:02:03 | `RegisterTaskDefinition alert-ingest:57` / `UpdateService`（github-actions-deploy） | E3 |
| 14:02:37 | 第一批新 task 启动，日志 `geoip client mode=sync cache=none … backoff_ms=0` | E5 |
| 14:03 | 处理速率开始下降（158→136/s），lag 离开基线（1,742）；enrich p99 9→199 ms | E1、E2、E6 |
| 14:04 | 第一批 429（406/min），DLQ 开始有消息 | E6、E8 |
| 14:05 | `report-renderer` CPU > 85%（14:07 告警），无关 | E11 |
| 14:06 | 8 个 task 全是新版本；处理速率 22/s 并保持 | E1 |
| 14:07:20 | 部署标记 COMPLETED（健康检查只看 `/healthz`） | E3、E12 |
| 14:10 | lag 首次 > 50,000 | E2 |
| 14:19 | `alert-ingest-consumer-lag-high` → ALARM（连续 10 个数据点），page | E0 |
| 14:30 | lag 209,844；最老未消费消息 1,380 s（≈23 min）；DLQ 3,232 | E2、E8 |

## 3. 证据

### E0 · 现在在响什么

```
$ python3 awsim.py alarms --table
2026-09-30T14:19:00Z  ALARM  alert-ingest-consumer-lag-high  (AWS/Kafka SumOffsetLag GreaterThanThreshold 50000)
2026-09-30T14:07:00Z  ALARM  report-renderer-cpu-high  (AWS/ECS CPUUtilization GreaterThanThreshold 85)
2026-09-30T13:01:00Z  OK     msk-broker-2-disk-high  (AWS/Kafka KafkaDataLogsDiskUsed GreaterThanThreshold 80)
2026-09-30T12:30:00Z  OK     geoip-svc-5xx-high  (Abnormal/GeoipSvc Http5xxCount GreaterThanThreshold 50)
```

### E1 · 进的平稳，出的塌了（消费端问题）

```
$ python3 awsim.py metrics get --namespace AWS/Kafka --name MessagesInPerSec --start 12:30 --end 14:31 --period 1800 --table
2026-09-30T12:30:00Z  151.47
2026-09-30T13:00:00Z  152.7
2026-09-30T13:30:00Z  153.89
2026-09-30T14:00:00Z  154.91
```

```
$ python3 awsim.py metrics get --namespace Abnormal/AlertIngest --name ProcessedPerSec --start 14:00 --end 14:08 --table
2026-09-30T14:02:00Z  158.32
2026-09-30T14:03:00Z  135.58
2026-09-30T14:04:00Z  98.54
2026-09-30T14:05:00Z  59.55
2026-09-30T14:06:00Z  22.26
2026-09-30T14:07:00Z  22.15
```

逐级下降是滚动部署的形状：新 task 两个一批上线，每批接走 2/8 的 partitions。

### E2 · lag 线性增长；换算成告警延迟

```
$ python3 awsim.py metrics get --namespace AWS/Kafka --name SumOffsetLag --stat Maximum --start 14:00 --end 14:13 --table
2026-09-30T14:02:00Z  152.14
2026-09-30T14:03:00Z  1742.47
…
2026-09-30T14:09:00Z  42391.1
2026-09-30T14:10:00Z  50258.22
2026-09-30T14:11:00Z  58174.57
```

```
$ python3 awsim.py metrics get --namespace AWS/Kafka --name EstimatedMaxTimeLag --stat Maximum --start 14:29 --end 14:31 --table
2026-09-30T14:30:00Z  1380.27
```

```
$ python3 awsim.py metrics get --namespace AWS/Kafka --name SumOffsetLag --stat Maximum --start 14:30 --end 14:31 --table
2026-09-30T14:30:00Z  209843.71
```

每分钟增量 ≈ (152 − 22) × 60 ≈ 7,800，与 14:10→14:11 的 +7,916 一致。1,380 s ≈ 23 分钟：**客户的告警现在晚了 23 分钟，而且每过一分钟再晚一分钟**。

### E3 · 拐点前 1 分钟的变更

```
$ python3 awsim.py deploys --start 13:00 --table
2026-09-30T13:58:41Z  report-renderer  report-renderer:112  2026.09.30-1358-b07c4de  render monthly PDFs in-process instead of shelling out to wkhtmltopdf
2026-09-30T14:02:03Z  alert-ingest  alert-ingest:57  2026.09.30-1402-a91f3c7  simplify geoip client
```

```
$ python3 awsim.py trail lookup --event-name UpdateService --table
2026-09-30T14:02:03Z  ecs.amazonaws.com  UpdateService  github-actions-deploy  {"cluster":"prod","service":"alert-ingest","taskDefinition":"alert-ingest:57","desiredCount":8}
```

```
$ python3 awsim.py deploys --service alert-ingest --start 14:00
…
      "completedAt": "2026-09-30T14:07:20Z",
…
      "previousTaskDefinition": "alert-ingest:56",
…
      "message": "simplify geoip client\n\nDrop the LRU cache and the batch lookup; call /v1/lookup once per record. Less code, one code path."
```

### E4 · 配置差异：去掉了批量、缓存、退避

```
$ python3 awsim.py config diff alert-ingest --table
~ geoip.mode: "batch" -> "sync"
~ geoip.batch_size: 500 -> 1
~ geoip.cache: "lru" -> "none"
~ geoip.backoff_ms: 250 -> 0
~ geoip.jitter: true -> false
- geoip.cache_ttl_s: 3600
```

### E5 · 运行中的版本确实是新 client（日志）

```
$ python3 awsim.py logs insights --group /ecs/alert-ingest --query 'filter message like "geoip client mode" | stats count() as n by version, message' --table
version=2026.09.29-1640-5e1d9b2  message=geoip client mode=batch cache=lru ttl=3600s batch_size=500 backoff_ms=250 jitter=true  n=8
version=2026.09.30-1402-a91f3c7  message=geoip client mode=sync cache=none batch_size=1 backoff_ms=0 jitter=false  n=8
```

```
$ python3 awsim.py logs insights --group /ecs/alert-ingest --query 'filter message like "geoip client mode=sync" | fields @timestamp, version | sort @timestamp asc | limit 1' --table
@timestamp=2026-09-30T14:02:37Z  version=2026.09.30-1402-a91f3c7
```

### E6 · 机制：请求暴涨 → 429 → 成功数钉在限额

```
$ python3 awsim.py metrics get --namespace Abnormal/AlertIngest --name GeoipRequestCount --stat Sum --start 14:01 --end 14:07 --table
2026-09-30T14:01:00Z  19.38
2026-09-30T14:02:00Z  19.24
2026-09-30T14:03:00Z  800.17
2026-09-30T14:04:00Z  1615.67
2026-09-30T14:05:00Z  2365.3
2026-09-30T14:06:00Z  3269.66
```

```
$ python3 awsim.py metrics get --namespace Abnormal/AlertIngest --name Geoip429Count --stat Sum --start 14:01 --end 14:07 --table
2026-09-30T14:03:00Z  0
2026-09-30T14:04:00Z  406.01
2026-09-30T14:05:00Z  1160.67
2026-09-30T14:06:00Z  2067
```

```
$ python3 awsim.py metrics get --namespace Abnormal/AlertIngest --name EnrichLatencyMs --stat p99 --start 14:01 --end 14:06 --table
2026-09-30T14:02:00Z  8.36
2026-09-30T14:03:00Z  198.98
2026-09-30T14:04:00Z  776.54
```

```
$ python3 awsim.py config show geoip-svc
      "alert-ingest": 1200,
```

14:03 只有 2 个新 task：800 次/min < 1,200，没有 429，但 p99 已是 ~200 ms（同步调用本身）；14:04 第 4 个新 task 上线，需求 1,616 > 1,200，429 出现。14:06 起 3,270 − 2,067 = 1,203 次成功/min——**就是限额**。

### E7 · 每条消息的代价（新旧版本并排）

```
$ python3 awsim.py logs insights --group /ecs/alert-ingest --query 'filter message = "consumed batch" | stats avg(enrich_ms_avg) as ms, sum(records) as recs, count_distinct(task) as tasks by version' --start 13:50 --end 13:51 --table
version=2026.09.29-1640-5e1d9b2  ms=2.94  recs=9648  tasks=8
```

```
$ python3 awsim.py logs insights --group /ecs/alert-ingest --query 'filter message = "consumed batch" | stats avg(enrich_ms_avg) as ms, sum(records) as recs, count_distinct(task) as tasks by version' --start 14:20 --end 14:21 --table
version=2026.09.30-1402-a91f3c7  ms=369.6  recs=1328  tasks=8
```

```
$ python3 awsim.py logs filter --group /ecs/alert-ingest --pattern 'status=429' --start 14:20 --end 14:21 --limit 1 --table
2026-09-30T14:20:00Z  app/86e4d3cea27d26934b484e73cf575dca  WARN  geoip lookup throttled status=429 attempt=2 elapsed_ms=162 retry_in_ms=0 (suppressed 42 similar in last 10s)
```

3 ms → 370 ms，约 125 倍；1,328 条/min = 22/s，与 `ProcessedPerSec` 一致。`retry_in_ms=0`：零退避立刻重试。

### E8 · DLQ：一成消息耗尽重试

```
$ python3 awsim.py logs filter --group /ecs/alert-ingest --pattern 'DLQ' --start 14:20 --end 14:21 --limit 1 --table
2026-09-30T14:20:01Z  app/86e4d3cea27d26934b484e73cf575dca  ERROR  enrichment failed after 5 attempts, message sent to DLQ topic=security-events partition=11 (suppressed 2 similar in last 10s)
```

```
$ python3 awsim.py metrics get --namespace AWS/SQS --name NumberOfMessagesSent --stat Sum --start 14:20 --end 14:21 --table
2026-09-30T14:20:00Z  134.79
```

```
$ python3 awsim.py metrics get --namespace AWS/SQS --name ApproximateNumberOfMessagesVisible --stat Maximum --start 14:03 --end 14:31 --period 900 --table
2026-09-30T14:30:00Z  3232.02
```

134.79 / 1,328 ≈ 10%。DLQ 里的 3.2k 条事件**不会**自己变成告警，回滚后要重放。

### E9 · 依赖本身健康：是我们的调用模式，不是 geoip-svc 坏了

```
$ python3 awsim.py metrics get --namespace Abnormal/GeoipSvc --name Http5xxCount --stat Sum --start 12:30 --end 14:31 --period 7200 --table
2026-09-30T12:00:00Z  0
2026-09-30T14:00:00Z  0
```

```
$ python3 awsim.py metrics get --namespace Abnormal/GeoipSvc --name ServerLatencyMs --stat p99 --start 12:30 --end 14:31 --period 7200 --table
2026-09-30T12:00:00Z  40.86
2026-09-30T14:00:00Z  40.8
```

```
$ python3 awsim.py metrics get --namespace Abnormal/GeoipSvc --name ThrottledCount --dim Client=risk-engine --stat Sum --start 12:30 --end 14:31 --period 7200 --table
2026-09-30T12:00:00Z  0
2026-09-30T14:00:00Z  0
```

```
$ python3 awsim.py config diff geoip-svc --table
(no differences)
```

### E10 · 红鲱鱼 1：broker-2 磁盘（早一小时，已恢复）

```
$ python3 awsim.py alarms --name msk-broker-2-disk-high --history
…
          "Timestamp": "2026-09-30T12:55:00Z",
…
          "Timestamp": "2026-09-30T13:01:00Z",
          "From": "ALARM",
          "To": "OK"
```

```
$ python3 awsim.py trail lookup --event-name UpdateBrokerStorage --table
2026-09-30T13:01:05Z  kafka.amazonaws.com  UpdateBrokerStorage  ops-dana  {"clusterArn":"arn:aws:kafka:us-east-1:111122223333:cluster/security-events-cluster/6a1f","targetBrokerEBSVolumeInfo":[{"kafkaBrokerNodeId":"2","volumeSizeGB":1500}]}
```

```
$ python3 awsim.py metrics get --namespace AWS/Kafka --name SumOffsetLag --stat Maximum --start 12:30 --end 14:00 --period 3600 --table
2026-09-30T12:00:00Z  284.09
2026-09-30T13:00:00Z  288.74
```

磁盘告警由 `ops-dana` 扩容 EBS 解决；12:30–14:00 的 lag 最大值 < 300，告警期间消费毫无反应。

### E11 · 红鲱鱼 2：report-renderer CPU（另一个集群）

```
$ python3 awsim.py describe ecs report-renderer
      "clusterArn": "arn:aws:ecs:us-east-1:111122223333:cluster/prod-batch",
…
      "note": "separate cluster, separate Fargate tasks: no CPU shared with prod"
```

```
$ python3 awsim.py metrics get --namespace AWS/ECS --name CPUUtilization --dim ServiceName=alert-ingest --start 12:30 --end 14:31 --period 3600 --table
2026-09-30T12:00:00Z  37.93
2026-09-30T13:00:00Z  37.99
2026-09-30T14:00:00Z  11.91
```

alert-ingest 的 CPU 是**下降**的：它在等网络，不缺 CPU。

### E12 · 红鲱鱼 3：RDS 空闲（被喂不饱，而不是瓶颈）；部署为什么"成功"了

```
$ python3 awsim.py metrics get --namespace AWS/RDS --name CPUUtilization --stat Maximum --start 12:30 --end 14:31 --period 7200 --table
2026-09-30T12:00:00Z  23.98
2026-09-30T14:00:00Z  22
```

```
$ python3 awsim.py metrics get --namespace AWS/RDS --name WriteIOPS --start 12:30 --end 14:31 --period 3600 --table
2026-09-30T13:00:00Z  1796.87
2026-09-30T14:00:00Z  491.02
```

```
$ python3 awsim.py describe ecs alert-ingest
      "healthCheck": "GET /healthz (process alive; does not look at consumer lag or enrichment errors)",
      "autoScaling": "none (fixed 8 tasks)"
```

```
$ python3 awsim.py describe msk security-events-cluster
      "Partitions": 12,
      "RetentionHours": 72
```

## 4. 根因

- **直接原因**：PR 4182（commit `a91f3c7`）把 enrichment 改成每条消息一次同步 `/v1/lookup`，删掉了缓存与批量，并把重试退避设为 0。
- **放大机制**：`geoip-svc` 对 `alert-ingest` 的配额是 1,200 rpm（20/s）；同步模式下每条消息至少一次调用，需求 ~3,270/min，六成以上被 429；零退避让每个 task 一直在热循环重试，平均每条 ~2.5 次调用 × ~150 ms ≈ 370 ms。整个 consumer group 的吞吐上限 = 配额 ≈ 20 条/s，远低于生产 ~150 条/s。
- **为什么没被拦住**：部署健康检查只看进程存活（`/healthz`）；没有 canary 指标门禁；没有对 429 的告警（`geoip-svc-5xx-high` 只看 5xx）；lag 告警需要 10 分钟 > 50k，从开始到 page 用了 16 分钟。

## 5. 止血

1. **回滚到 `alert-ingest:56`**（14:30 决定；滚动约 5 分钟，参考 E3 的 14:02:03→14:07:20）。
2. 不扩容：成功数被配额钉死；12 partitions 封顶 12 个活跃 consumer。按日志里每次调用 ~150 ms 估算：12 tasks → 4,800 次/min，成功 1,200 → 每次成功概率 0.25 → 吞吐 ~26 条/s，DLQ 率 0.75⁵ ≈ 24%（现在 0.625⁵ ≈ 9.5%）。
3. 验证：`ProcessedPerSec` 远高于 `MessagesInPerSec`（追赶）、`Geoip429Count` 归零、`SumOffsetLag` 斜率转负、`EstimatedMaxTimeLag` 回到秒级。追赶期间盯 RDS `WriteIOPS` / `WriteLatency`：追赶速率可达平时十几倍。
4. lag 清空后**重放 DLQ**（3,232 条），写库按事件 ID 幂等。
5. 沟通：频道里发 5 行 summary（见 `investigation.md` §7），每 15 分钟更新到 lag 清零与 DLQ 重放完成。

## 6. 长期修复

| 类别 | 行动 | 解决什么 |
|---|---|---|
| 代码 | 恢复批量 + 本地 LRU 缓存；或把 mmdb 嵌进 consumer（去掉每条消息的网络调用） | 调用量与吞吐解耦 |
| 代码 | 429 尊重 `Retry-After`；指数退避 + 抖动；重试预算（retry budget）；熔断 | 不再热循环，不再把限流放大成 DLQ |
| 部署 | canary 1 task + 自动比较 `ProcessedPerSec`、`EnrichLatencyMs`、429 率；失败自动回滚 | 本次 2 分钟内就能拦住 |
| 部署 | 健康检查反映工作质量（最近 N 秒有成功处理、错误率阈值） | ECS circuit breaker 才有意义 |
| 告警 | 依赖 429 率、DLQ 入队速率；`ProcessedPerSec / MessagesInPerSec < 0.8` 持续 3 分钟（本快照 14:06 触发）；lag 用时间（`EstimatedMaxTimeLag` 对应 SLO） | 发现时间从 16 分钟缩到 3 分钟 |
| 容量 | 文档化"每条消息对下游的调用数 × 生产速率 ≤ 下游配额"；评审清单加"是否改变了对下游的调用量" | 让这类改动在 PR 阶段被问出来 |
| 测试 | geoip client 负载测试：按生产速率跑 1 分钟，断言请求数 ≤ 配额 | 回归保护 |

## 7. Postmortem 行动项（owner 为角色）

| # | 行动 | Owner | 优先级 |
|---|---|---|---|
| 1 | 恢复批量 + 缓存，加退避/抖动/熔断，再发布（带 canary） | alert-ingest owner | P0 |
| 2 | 429 率与 DLQ 速率告警；lag 告警改为时间 SLO | alert-ingest on-call | P0 |
| 3 | ECS 部署加 canary 指标门禁 + 有意义的健康检查 | platform | P1 |
| 4 | DLQ 重放 runbook（幂等前提、限速） | alert-ingest owner | P1 |
| 5 | 内部服务配额目录 + PR 模板中的"下游调用量"一栏 | platform + geoip-svc owner | P2 |

## 8. 英文口播（90 s 总结）

> "At 14:02 we deployed alert-ingest 57, which replaced batched, cached geoip lookups with one synchronous call per message and zero-backoff retries. Request volume to geoip-svc went from about 20 a minute to over 3,000, geoip-svc's per-client limit of 1,200 a minute started returning 429s, and successful lookups were pinned at exactly that limit — 20 a second, against 150 a second of input. Processing fell from 160 to 22 messages a second, lag grows by about 7,800 a minute, and alerts are now about 23 minutes late, with roughly one in ten events going to the DLQ. The other alarms are unrelated: report-renderer is in a separate cluster, the broker disk alarm resolved an hour before, and RDS is idle. Scaling out won't help because the limit caps successes and we only have 12 partitions. So I'm rolling back to 56, I'll watch processed-per-second and the lag slope, then redrive the DLQ. Long term: restore batching and caching, back off on 429s, add a canary gate on throughput, and alert on dependency throttling and on lag measured in minutes."
