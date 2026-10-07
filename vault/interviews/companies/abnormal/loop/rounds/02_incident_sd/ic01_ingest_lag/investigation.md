# ic01 · 推荐排查路径（alert-ingest consumer lag）

> 系统：MSK(Kafka) topic `security-events`（12 partitions）→ ECS 服务 `alert-ingest`（8 tasks，consumer group `alert-ingest`）→ enrichment 调内部 `geoip-svc` → 写 Postgres `alerts-prod`；enrichment 失败的消息进 SQS `security-events-dlq`。
> 本文讲**怎么走**；每一步看到的具体数字在 `model_answer.md`。所有命令在本目录运行。

## 0. 前 2 分钟：先问、先定框（不碰控制台）

面试官给你 page 之后，先把"事故管理"的框说出来，再开始翻。三个问题：

1. **影响面**（impact）：lag 意味着什么？——客户的安全告警**延迟**生成（Abnormal 的产品价值就是及时告警），不是数据丢失（Kafka retention 72 h）。要问：有没有客户可见的 SLO？DLQ 里的消息是不是"永远不会变成告警"？
2. **开始时间**（onset）：告警是 14:19 触发的，但条件是"连续 10 分钟 > 50k"，真实开始更早——要从图上找拐点，不是从告警时间推。
3. **最近变更**（recent changes）：部署、配置、基础设施操作（CloudTrail）。绝大多数事故是变更引起的。

> 🗣️ "Before I dig in: lag here means customers' security alerts are delayed, not lost — retention is 72 hours. So the clock that matters is how stale alerts are. I want three things first: when did it actually start — the alarm needs 10 minutes over threshold so the onset is earlier — what changed around then, and is it a producer-side spike or a consumer-side slowdown."

同时说一句沟通安排：

> 🗣️ "I'd open an incident channel, post that I'm investigating, and commit to an update every 15 minutes."

## 1. 先分清：生产变多了，还是消费变慢了？

lag = 进 − 出。第一刀永远是把这个等式拆开：

```
python3 awsim.py alarms --table                       # 现在有哪些告警在响？（会看到另一个 ALARM：先记下，别追）
python3 awsim.py metrics get --namespace AWS/Kafka --name SumOffsetLag --stat Maximum --start 13:50 --end 14:31 --table
python3 awsim.py metrics get --namespace AWS/Kafka --name MessagesInPerSec --start 12:30 --end 14:31 --period 1800 --table
python3 awsim.py metrics get --namespace Abnormal/AlertIngest --name ProcessedPerSec --start 13:58 --end 14:10 --table
python3 awsim.py metrics get --namespace AWS/Kafka --name EstimatedMaxTimeLag --stat Maximum --start 14:25 --end 14:31 --table
```

要得出的结论：**进的速率平稳，出的速率在 14:03–14:06 之间掉了一个数量级** → 消费端问题。lag 是一条直线（每分钟增量≈常数），说明是"稳态吞吐不足"，不是一次性的卡顿。`EstimatedMaxTimeLag` 把 lag 翻译成"告警延迟了多少分钟"——这是给状态更新用的数字。

> 🗣️ "Input is flat at about 150 messages a second; processing fell from about 160 to about 22 between 14:03 and 14:06, and lag is growing in a straight line. So this is a consumer throughput collapse, not a traffic spike, and it won't recover on its own."

## 2. 拐点对上了什么变更？

```
python3 awsim.py deploys --start 13:00 --table
python3 awsim.py trail lookup --start 13:30 --table
python3 awsim.py config diff alert-ingest
```

14:02:03 有 `alert-ingest` 的部署，commit 写着 "simplify geoip client"；config diff 显示 `mode batch→sync`、`cache lru→none`、`backoff_ms 250→0`、`jitter true→false`。13:58 另有 `report-renderer` 的部署——**记下来，但要用证据排除，不是靠直觉**。

> 🗣️ "There's an alert-ingest deploy at 14:02, one minute before the inflection, and the config diff removes batching, the cache and the retry backoff from the geoip client. That's my leading hypothesis: per-message synchronous geoip calls. Let me confirm the mechanism instead of assuming it."

## 3. 确认机制：每条消息为什么变慢？

假设链：同步调用 → 请求量暴涨 → `geoip-svc` 限流（429）→ 客户端零退避重试 → 每条消息耗时 ×100 → 吞吐崩。逐环验证：

```
python3 awsim.py metrics get --namespace Abnormal/AlertIngest --name EnrichLatencyMs --stat p99 --start 14:00 --end 14:08 --table
python3 awsim.py metrics get --namespace Abnormal/AlertIngest --name GeoipRequestCount --stat Sum --start 14:00 --end 14:08 --table
python3 awsim.py metrics get --namespace Abnormal/AlertIngest --name Geoip429Count --stat Sum --start 14:00 --end 14:08 --table
python3 awsim.py logs insights --group /ecs/alert-ingest --query 'filter message = "consumed batch" | stats avg(enrich_ms_avg) as ms, sum(records) as recs, count_distinct(task) as tasks by version' --start 14:20 --end 14:21 --table
python3 awsim.py logs insights --group /ecs/alert-ingest --query 'filter level != "INFO" | stats count() as n by level, bin(5m)' --start 13:50 --end 14:10 --table
python3 awsim.py logs filter --group /ecs/alert-ingest --pattern 'status=429' --start 14:20 --end 14:21 --limit 3 --table
python3 awsim.py config show geoip-svc
```

用 logs insights 缩小范围的套路：**先 `stats count() by level, bin(5m)` 看错误何时出现，再 `by version` 把新旧版本放在一起比**。新版本的日志行自带 `retry_in_ms=0`——零退避直接写在日志里。

最关键的一步是**算账**：`GeoipRequestCount − Geoip429Count` ≈ 1,200/min，正好等于 `geoip-svc` 给这个 client 的限额 `1200 rpm`。成功查询被钉死在 20/s，而生产是 ~150/s——这一个数就解释了吞吐上限。

> 🗣️ "Successful lookups are pinned at exactly 1,200 a minute — that's geoip-svc's per-client limit. Every message now needs one lookup, so the whole consumer group can't enrich more than 20 messages a second while 150 arrive. The client retries 429s with zero backoff, so each message burns about two and a half attempts at roughly 150 ms each, and about one in ten exhausts five attempts and goes to the DLQ."

## 4. 反事实：为什么不是红鲱鱼

每个可疑信号都用"如果它是原因，我应该还能看到什么？"来排除：

| 信号 | 如果它是原因，应当看到 | 实际 | 命令 |
|---|---|---|---|
| `report-renderer-cpu-high`（14:07 ALARM） | alert-ingest 与它共享 CPU；alert-ingest CPU 高 | renderer 在 `prod-batch` 集群、独立 Fargate task；alert-ingest CPU 从 ~38% **降**到 ~8%（在等网络，不在算） | `describe ecs report-renderer`、`metrics get --namespace AWS/ECS --name CPUUtilization --dim ServiceName=alert-ingest` |
| MSK broker-2 磁盘告警 | 告警期间 lag 上升；告警持续到 14:00 后 | 12:55 ALARM → 13:01 OK（扩容 1000→1500 GiB，CloudTrail 有 `UpdateBrokerStorage`）；那段时间 lag 平稳 | `alarms --name msk-broker-2-disk-high --history`、`trail lookup --event-name UpdateBrokerStorage` |
| RDS 慢 | 写延迟上升、CPU 高、连接数涨 | CPU < 25%，WriteIOPS 反而**下降**（消费者喂不饱它） | `metrics get --namespace AWS/RDS --name WriteIOPS` |
| `geoip-svc` 自己坏了 | 5xx、服务端延迟上升、另一个 client 也被拒 | 5xx = 0，服务端 p99 ~40 ms，`risk-engine` 的 ThrottledCount = 0；`geoip-svc` 最近部署是 09-17 | `metrics get --namespace Abnormal/GeoipSvc ...` |

注意那条**告警空白**：`geoip-svc-5xx-high` 一直 OK——429 不是 5xx，没有任何告警盯着限流。这是长期修复里的一条。

> 🗣️ "The other alarm is report-renderer, which runs in a separate cluster; alert-ingest's CPU actually dropped, which is what you'd expect if it's waiting on the network. geoip-svc itself is healthy — no 5xx, flat latency, the other client isn't throttled. It's doing exactly what its rate limit says. The problem is our new call pattern."

## 5. 止血：选项与取舍（先止血，再完善根因）

**根因确认到"足以行动"就行动**——不需要等完全证明。到第 3 步结束（约 10 分钟）就应该提出回滚。

| 选项 | 效果 | 风险 / 为什么不选 |
|---|---|---|
| **回滚到 `alert-ingest:56`**（推荐） | 恢复批量 + 缓存 + 退避；旧版本 enrich ~3 ms/条（单线程约 300 条/s/task），8 tasks 的余量远大于生产 ~150/s | 回滚本身要 ~5 min（上次滚动部署 14:02:03→14:07:20）；回滚期间新旧混跑。需确认 :56 与当前 schema/topic 兼容（commit 只改了 geoip client，可以） |
| 扩 consumer（加 task） | **几乎无效，且更糟**：成功查询被 1,200 rpm 钉死；12 partitions 封顶 12 个活跃 consumer；12 tasks 时吞吐 ~26 msg/s，但 DLQ 率从 ~9.5% 升到 ~24% | 加剧对共享依赖的压力；rebalance 期间吞吐进一步下降 |
| 请 `geoip-svc` 临时提额 | 可能直接解除瓶颈 | 是别人的服务、别人的容量；限流就是为了保护它与 `risk-engine`；需要对方同意，且治标 |
| 暂停消费 / 跳过 enrichment（feature flag 降级） | 如果有"无 geo 也能出告警"的开关，可先恢复告警及时性 | 本快照里没有这个 flag（`config diff` 里没有）；降级告警质量要产品同意 |

> 🗣️ "Mitigation first: roll back alert-ingest to task definition 56. Scaling out won't help — successful lookups are capped by the rate limit, and with 12 partitions I can't run more than 12 active consumers anyway; my arithmetic says 12 tasks gets us from 22 to about 26 messages a second while the DLQ rate more than doubles. Asking geoip-svc for a higher limit is a fallback, not a first move: it's someone else's capacity."

回滚后的验证（说出来）：`ProcessedPerSec` 回到 >150 并在追赶期远高于生产；`Geoip429Count` 归零；lag 斜率转负；然后**重放 DLQ**（~3.2k 条）——前提是写库幂等。追赶期间盯 RDS 写入：追赶速率可能是平时的十几倍。

## 6. 长期修复（按"防止再发生 / 更早发现 / 更快恢复"分组）

- **代码**：恢复批量 + 本地 LRU 缓存（IP 地理信息变化慢，命中率高）；对 429 尊重 `Retry-After`，带抖动的指数退避（exponential backoff with jitter）+ 重试预算；熔断（circuit breaker）；更进一步把 MaxMind mmdb 嵌进 consumer 进程，去掉每条消息的网络调用。
- **部署门禁**：canary（先 1 个 task）+ 自动比较 `ProcessedPerSec` / `EnrichLatencyMs` / 429 率；ECS health check 只看 `/healthz`，所以这次部署"成功"了——健康检查要反映真实工作。
- **告警**：对 429 率与 DLQ 入队速率告警；lag 告警改用 `EstimatedMaxTimeLag`（分钟数对应产品 SLO）而不是绝对条数；`ProcessedPerSec / MessagesInPerSec < 0.8 持续 3 分钟` 在本快照里 14:06 就会触发，比 "10 分钟 > 50k"（14:19）早 13 分钟。
- **容量**：写下 consumer 吞吐 SLO 与依赖配额的关系（每条消息调用数 × 生产速率 ≤ 下游配额）；代码评审清单加一条"这个改动改变了对下游的调用量吗？"。
- **Runbook**：lag 告警 runbook 第一步 = 进出速率拆分 + 最近部署 + 依赖 429。
- **测试**：对 geoip client 的负载测试（以生产速率跑 1 分钟，断言请求数 ≤ 配额）。

## 7. 5 行 incident summary（写给频道）

```
[RESOLVED-PENDING] alert-ingest consumer lag — security alerts delayed up to ~23 min
Impact: 14:03–(rollback) UTC, alert generation delayed (max ~23 min at 14:30); ~3.2k events in DLQ, no data lost (72 h retention).
Cause: deploy alert-ingest:57 (14:02, "simplify geoip client") made one sync geoip call per message with zero-backoff retries;
       geoip-svc's 1,200 rpm per-client limit capped enrichment at ~20 msg/s vs ~150 msg/s produced.
Mitigation: rolled back to alert-ingest:56; lag draining; DLQ redrive after drain. Next update in 15 min.
```

## 8. 自查清单（做完对照）

- [ ] 2 分钟内说出了影响面（延迟 ≠ 丢失）与三问
- [ ] 用进/出速率拆分 lag，而不是先翻日志
- [ ] 找到 14:02 部署并**验证机制**（429、成功数 = 限额）
- [ ] 算出"扩容无效"的数（限额 20/s、12 partitions）
- [ ] 至少排除 2 个红鲱鱼，并说出排除依据
- [ ] 10–12 分钟内提出回滚，并说出回滚后的验证指标
- [ ] 指出告警空白（429 不是 5xx）与健康检查过浅
