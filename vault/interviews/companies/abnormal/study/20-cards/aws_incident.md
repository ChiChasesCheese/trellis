# 速记卡 · AWS 环境排查（Incident 轮用；与 ic01 / ic02 配套）

> 原话（#8496901）："What was going wrong · How I would identify the root cause · What signals/logs/monitoring tools · immediate mitigation · long-term fixes"。JD："Strong debugging skills with logs, metrics, and behavioral signals"。

1. **前 2 分钟只问不点**：影响面（谁、多少、哪个功能）· 什么时候开始（精确到分钟）· 最近变了什么（部署、配置、迁移、流量、证书）· 现在还在恶化吗。英文："Before I click anything: what's the customer impact, when exactly did it start, and what changed around then?"
2. **先止血后根因**：能回滚 / 关 flag / 限流就先做，同时并行查根因。说出止血的风险与回退方式。
3. **按变更时间线对齐**：部署记录（ECS/K8s 任务定义版本、commit message）、CloudTrail（`UpdateService`、`ModifyDBInstance`、`ImportCertificate`、`UpdateBrokerStorage`）、迁移流水线。症状开始时间 ±2 分钟内的变更是第一嫌疑。
4. **CloudWatch 指标看形状**：阶跃（变更）、线性增长（速率不匹配：生产 > 消费）、锯齿（重试/超时）、平顶（上限：池、限流、连接数）。
5. **队列/流的四个数**：lag（MSK `SumOffsetLag`）、最老消息年龄（`EstimatedMaxTimeLag` / SQS `ApproximateAgeOfOldestMessage`）、消费速率、DLQ 深度。lag 线性涨 = 消费速率永久低于生产速率。
6. **Logs Insights 套路**：`filter level="ERROR" | stats count() by bin(1m)` 看何时开始；`stats count() by error_type, version` 看是不是新版本才有；`stats pct(latency_ms, 99) by route` 看哪个端点。采样日志用 `sum(sample_rate)` 估算。
7. **ALB 指标**：`HTTPCode_Target_5XX`（应用返回）vs `HTTPCode_ELB_5XX`（502/503/504：目标不可用或超时）；`TargetResponseTime` p99。504 + 应用 CPU 低 = 在等东西（锁、连接池、下游）。
8. **RDS**：`DatabaseConnections`（是否贴 max）、`ReadIOPS`/`WriteIOPS`、CPU；Performance Insights 看等待事件（`Lock:relation` = 锁；`IO:DataFileRead` = 缺索引的扫描）；`pg_stat_activity` 看谁持锁。
9. **红鲱鱼的排除话术**："It alarmed, but it started an hour earlier / it's in another cluster / its metric moved the other way — so it's not the cause."
10. **扩容的陷阱**：下游限流（429）或锁/连接池上限时，加实例只会更糟（更多 429、更多连接）。先问"瓶颈在哪一层"。
11. **长期修复的五类**：代码（缓存/批量/退避/熔断）· 发布（canary 指标门禁、迁移规范：`CREATE INDEX CONCURRENTLY`、`lock_timeout`、分批回填、发布顺序）· 告警（429 率、lag、最老消息年龄，而不只是 5xx）· 容量（限额、池大小 vs `max_connections`）· runbook 与 postmortem 行动项（有 owner 有日期）。
12. **5 行 incident summary**：Impact · Timeline（UTC）· Root cause · Mitigation · Follow-ups。
