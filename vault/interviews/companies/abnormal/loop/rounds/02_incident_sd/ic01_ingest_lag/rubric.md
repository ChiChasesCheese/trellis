# ic01 · Rubric（alert-ingest consumer lag）

> 面试官关心的原话（#8496901 Round 3）："not just in finding the issue, but also in how I approached debugging and how I prioritized short-term mitigation vs. long-term remediation." 按下表逐行自评；"strong" 每行都要有一个你说出口的具体数字或命令。

| 维度 | strong | ok | weak |
|---|---|---|---|
| 开场与定框 | 2 分钟内说出：lag = 告警延迟不是丢失（retention 72 h）；告警需 10 分钟持续，真实开始更早；要查最近变更；开事故频道并承诺更新节奏 | 问了开始时间与变更，但没说影响面 | 直接开始翻日志 |
| 调试方法 | 假设驱动：先拆 lag = 进 − 出（`MessagesInPerSec` 平、`ProcessedPerSec` 160→22），再对拐点找变更（14:02 部署），再逐环验证机制（请求量 → 429 → 成功数 = 1,200 rpm 配额） | 找到部署并看到 429，但没算出"成功数 = 配额"这一锚点 | 按控制台顺序逐个看图；或看到部署就宣布根因，不验证机制 |
| 用 logs insights 缩小 | `stats count() by level, bin(5m)` 定位错误起点；`by version` 新旧版本并排比较 enrich 耗时（3 ms vs 370 ms）；注意到 `retry_in_ms=0` | 用 filter 找到 429 日志 | 只用 `tail` 翻日志 |
| 红鲱鱼处理 | 对每个可疑信号说"如果它是原因我还应看到什么"：renderer 在 `prod-batch` 且 alert-ingest CPU 反降；broker-2 告警 13:01 已恢复且 lag 当时平稳；RDS CPU < 25%、WriteIOPS 下降；geoip-svc 5xx=0、另一个 client 未被限流 | 排除了 1–2 个但理由是"时间对不上"之类的直觉 | 去追 report-renderer 告警，或认为 geoip-svc 坏了要对方修 |
| 止血优先 | ~10–12 分钟内提出回滚 `alert-ingest:56`；用数字否定扩容（配额钉死 20/s；12 partitions 封顶；12 tasks 只到 ~26/s 且 DLQ 率 9.5%→24%）；说出回滚后看哪些指标确认、DLQ 重放与幂等、追赶期盯 RDS | 提出回滚但没说为什么不扩容，或没说验证指标 | 先"把根因彻底查清"再止血；或提出加 task / 要求 geoip-svc 提额作为第一步 |
| 沟通（状态更新） | 给出 5 行状态更新（影响：告警延迟 ~23 min 且每分钟再晚 1 min、DLQ 3.2k；原因；动作；下次更新时间）；讲话先结论后证据 | 有更新但缺影响或下一步 | 不提沟通，或只说技术细节 |
| 长期修复质量 | 按"防再发 / 早发现 / 快恢复"分组：批量 + 缓存或进程内 mmdb、429 尊重 `Retry-After` + 抖动退避 + 重试预算 + 熔断；canary 指标门禁与有意义的健康检查；429 率、DLQ 速率、进出比告警，lag 按时间 SLO；"下游调用量"进评审清单；负载测试 | 列了退避、缓存、告警，但不成体系 | "加监控""加机器" |
| 指出系统性缺口 | 点名 3 个让事故溜过去的缺口：健康检查只看 `/healthz`、没有 canary 门禁、429 不是 5xx 所以没有告警 | 点名 1 个 | 无 |

## 常见失分（按出现频率）

1. 看到 `report-renderer-cpu-high` 在 ALARM 就先去查它（它更"响"，但在另一个集群）。
2. 说"consumer 不够，扩到 16 个 task"——忽略配额与 partition 数；面试官会追问"扩完会怎样"。
3. 把 `geoip-svc` 当成故障方："geoip-svc is returning errors, page their on-call"——它在按配置限流，问题是调用方。
4. 只说"回滚"不说回滚后的验证与 DLQ 重放；或忘了重放要求写库幂等。
5. 长期修复只有"加退避"，没有部署门禁与告警空白。

## 时间分配（30 min 的 incident 部分）

| 分钟 | 应完成 |
|---|---|
| 0–2 | 定框：影响面、三问、沟通节奏 |
| 2–6 | 进/出拆分，确认消费端问题；找到 14:02 部署与 config diff |
| 6–11 | 验证机制（429、成功数 = 配额、每条 370 ms），排除至少 2 个红鲱鱼 |
| 11–13 | 提出回滚 + 否定扩容的算术 + 验证指标 |
| 13–25 | 长期修复、告警空白、postmortem 行动项 |
| 25–30 | 5 行 summary + 回答追问 |
