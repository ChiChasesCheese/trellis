# sd01 · Scale an existing system: the security-events pipeline

> 原话（#8496901 Round 3 part 2）："I was given an **existing system** and asked how I would scale it … Scaling reads · Scaling writes · Identifying bottlenecks · how the existing architecture would behave as traffic increased." 系统本身 **(reconstructed)**：就是 `../../01_ai_screen/cb01_sentinel/` 的架构（报道过的 AI screen 代码库形态），这样 screen 里建立的心智模型可以直接复用。
> 45 min：5 min 澄清 → 10 min 现状瓶颈 → 20 min 方案（写/读/状态）→ 10 min 失败与演进。

## The prompt (as the interviewer would say it)

Here is our security-events pipeline today:

```
collectors (auth logs, endpoint, SaaS audit; pull every 60 s per tenant)
   │  JSON events, ~1 KB each
   ▼
single Kafka topic `events` (12 partitions, keyed by tenant_id)
   ▼
pipeline workers (Python, 6 pods)  ── per event:
   ├─ geo-ip enrichment: HTTP call to geoip-svc
   ├─ history enrichment: SELECT … FROM user_history WHERE tenant_id=? AND user=?   (Postgres primary)
   ├─ threat-intel enrichment: HTTP call to intel-svc
   ├─ rules (brute_force keeps a 10-min window: SELECT count(*) FROM events WHERE … )
   └─ INSERT event row; INSERT alert row if any rule hits      (same Postgres primary)
   ▼
Postgres (one primary, db.r6g.2xlarge): events, user_history, alerts
   ▲
alerts API (analyst console): GET /alerts?tenant=…&status=OPEN ORDER BY score DESC LIMIT 50 OFFSET n
```

Today: ~2,000 events/s at peak across ~300 tenants; alerts API p99 is 2 s and climbing.
Next quarter a very large customer onboards; we expect **~50,000 events/s at peak**, and one tenant will be ~40% of traffic.
**How would you scale this? Walk me through reads, writes, and where it breaks first.**

## What you can ask (interviewer answers if asked)

- Latency target from event to alert? → "Under a minute is fine; under 10 s would be great for login-based detections."
- Do analysts search raw events? → "Yes, in the alert detail view and in investigations, last 30 days."
- Retention? → "Events 30 days hot, a year cold for compliance. Alerts forever."
- Can we lose events? → "No. Duplicated alerts are annoying; missed alerts are an incident."
- Ordering requirements? → "Per user, roughly — brute-force and impossible-travel reason over a user's sequence."

## 中文题意

上图是现有的安全事件管线：采集器每 60 秒按租户拉取（每条 ~1 KB JSON）→ 单个 Kafka topic（12 个分区，按 tenant_id 分区）→ 6 个 Python worker，每条事件：HTTP 调 geoip-svc、查 Postgres 的用户历史、HTTP 调 intel-svc、brute_force 规则用 `count(*)` 查 10 分钟窗口、写事件行、命中则写告警行（同一个 Postgres 主库）→ 分析师用的告警 API（`ORDER BY score DESC LIMIT 50 OFFSET n`）。
现状：峰值 ~2,000 事件/秒、~300 租户；告警 API p99 = 2 s 且在变差。下季度一个超大客户接入：峰值 **~50,000 事件/秒**，单个租户占 ~40% 流量。**问：怎么扩容？读、写分别怎么办，哪里先坏？**
可问到的答案：事件→告警延迟 1 分钟内可接受（登录类最好 10 s 内）；分析师要搜 30 天内原始事件；事件热存 30 天、冷存 1 年、告警永久；不能丢事件（重复告警可以忍，漏告警是事故）；同一用户的事件大致要有序。
