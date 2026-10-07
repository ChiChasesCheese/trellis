# ic02_api_5xx · REPORT

告警 "portal-api 5xx rate > 5% and p99 > 3 s"。根因（reconstructed），两阶段：**A** 09:40:07–09:52:14 迁移 `0142_alerts_timeline` 在一个事务里 `ALTER TABLE alerts ADD COLUMN` + 非 `CONCURRENTLY` 的 `CREATE INDEX`，`ACCESS EXCLUSIVE` 锁持有 12 分钟 → 240 个池连接全在等锁 → 5xx ~70%；**B** 流水线 720 s 超时杀掉迁移、事务回滚，锁释放但新端点 `/timeline` 需要的索引没建 → 读 IO 贴 12k、池仍满 → 5xx ~7.6%、平均 2.08 s。练习者在 10:05（阶段 B 中）接手；止血 = 关 flag `timeline_v2`。

## 快照规模（`env/`，确定性生成）

| 项 | 数 |
|---|---|
| 文件 / 字节 | 69 / 2,180,819 |
| 时间窗 | 2026-10-02T08:30:00Z → 10:05:00Z（96 分钟） |
| 指标 | 5 个命名空间、26 个指标文件、3,604 个数据点 |
| 日志 | 3 个 log group（应用、迁移任务、RDS Postgres）、26 个 stream、5,389 行；应用请求日志按 `sample_rate` 采样（正常 1/1000，慢或 5xx 1/100） |
| CloudTrail / 部署 / 告警 | 12 / 4（含 1 条迁移记录）/ 5 |
| 配置 / 资源描述 | 6 / 7（elbv2、ecs×2、rds、pg 表统计、Performance Insights、迁移文件） |

ALB 计数逐分钟自洽：`RequestCount = 2XX + 4XX + Target 5XX + ELB 5XX`（测试断言误差 < 0.1）。

## 红鲱鱼

1. 09:37:50 / 09:38:20 导入新证书并换 ALB listener：TLS 握手错误 ≤ 2/min，换证后两分钟 0 错误，错误类型是 503/504。
2. `tn-orbit` 流量 09:00–09:20 翻倍：此后 20 分钟无错误；阶段 B 有 9 个租户出 5xx——放大器（38.1M 行），不是原因。
3. 09:35–09:43 的 4xx 突增：`portal-web` 先于 API 上线，调用尚不存在的 `/timeline` 得到 404；与 5xx 无因果，但是 postmortem 里的发布顺序问题。
4. portal-api CPU 下降（~33% → 7–15%）：按 CPU 的 autoscaling 不会触发；扩容只会多占连接。
5. "锁已释放"本身是陷阱：只找到阶段 A 的人会以为事故在 09:52 结束。

## 测试（`→ 78 passed`）

| 文件 | `def test` | 收集数 | 内容 |
|---|---|---|---|
| `test_ic02_awsim.py` | 17 | 17 | 查询子集（独立副本） |
| `test_ic02_story.py` | 15 | 15 | 时间戳；ALB 计数自洽；迁移单事务、无 CONCURRENTLY、被杀、回滚；锁等待窗口与持锁 pid；池与 max_connections；阶段 B 改善但不恢复；索引缺失；红鲱鱼无害 |
| `test_ic02_model_answer.py` | 3 | 46 | `model_answer.md` 的 44 个证据块（124 行输出）逐条重跑比对 |

## 已知弱点

1. 阶段 B 的错误/延迟按路由是手设比例加噪声，不是排队模型：p99 两阶段都约 10.07 s（池超时），RDS 连接平在 292/293，Postgres 锁等待日志约每 5 s 一条（真实会多得多）。
2. 采样日志与 ALB 指标只是同量级：09:55–10:05 日志估算约 1,200 个 client-disconnected 500，ALB `HTTPCode_ELB_504_Count` 约 1,460。
