# ic02 · Rubric（portal-api 5xx + p99）

> 面试官关心的原话（#8496901 Round 3）："not just in finding the issue, but also in how I approached debugging and how I prioritized short-term mitigation vs. long-term remediation." 本题的区分点是**两个阶段**：找到锁就收工的人拿不到 strong。

| 维度 | strong | ok | weak |
|---|---|---|---|
| 开场与交接 | 从"09:52 好了很多然后一直不好"推出两阶段假设；问影响面（全租户？全端点？）、现在 vs 峰值、同事做过什么；承诺更新节奏 | 问了影响面和变更，没抓住交接线索 | 直接翻日志；或把交接话当噪音 |
| 读懂 ALB 信号 | 区分 Target 5XX（应用 503）与 ELB 5XX（ALB 504）；认出 p99 ≈ 10 s 是 `pool_timeout` 的天花板；说清 10 s / 15 s / 30 s 三个超时 | 看到 5xx 与延迟，但不分来源 | 只看 RequestCount 或只看 p99 |
| 调试方法（阶段 A） | 拐点对变更：`RunTask` 09:40:05 / `StopTask` 09:52:10 正好对应两个拐点；用 PI / 锁等待日志找到 pid 40117 与 relation 16421 = `alerts`；说出"ALTER 本身 4 ms，但锁持有到事务结束，事务里还有 12 分钟的非并发建索引" | 找到迁移与锁，但机制说不清（以为 ALTER 本身慢） | 归因于"数据库挂了 / 流量大" |
| 共享池洞察 | 指出 `/users/{id}/risk` 不碰 `alerts` 也全部 503 → 共享连接池耗尽；DB CPU ~25% 而负载 ~270 会话 → 都在等锁；Little 定律：240 连接 / 30 s ≈ 8 请求/s | 说"连接池满了" | 无 |
| 阶段 B（区分点） | 主动问"锁没了，什么还在耗 DB"；PI top SQL = timeline 查询、`IO:DataFileRead`、ReadIOPS 贴 12k；auto_explain `Rows Removed by Filter ~4M`；`describe pg` 无 `user_id` 索引；把它连回"迁移回滚 = 索引没建" | 找到慢查询但没连回迁移回滚 | 认为 09:52 后是"余波"、会自己恢复 |
| 红鲱鱼处理 | 证书：TLS 错误 ≤ 2/min、换证书后两分钟 0 错误、错误类型是 503/504；`tn-orbit`：翻倍后 20 分钟无错误、9 个租户都出错 → 放大器；4xx 突增是前端先上线 | 排除了其一 | 追证书轮换；或"限流 tn-orbit"当根因修复 |
| 止血优先 | 10:05 选关 flag `timeline_v2`（最窄最快）；说出回滚是备选及其代价；用连接账否定加池 / 扩容（可用 245、已用 240、12×30=360；09:40 已出现 `remaining connection slots`）；说出验证指标；补索引用 `CONCURRENTLY` + `lock_timeout`，确认 `indisvalid`，再按租户逐步开 flag；顺带说出阶段 A 若在场应 `pg_terminate_backend(40117)` | 提出关 flag 或回滚，但没否定加池 | "把 pool 调大""加 task""重启服务" |
| 沟通 | 5 行状态更新（两阶段影响、原因、正在做的、下次更新时间）；告知前端团队 | 有更新但缺下一步 | 无 |
| 长期修复质量 | 迁移规范（CONCURRENTLY、DDL 不与建索引同事务、`lock_timeout`、分步回填、CI lint）；发布顺序（迁移成功才生效、前端晚于后端）；超时梯度（应用 < ALB）；连接预算 + RDS Proxy/PgBouncer；舱壁分池；锁等待 / PI 告警；按租户限流 | 只有"加 CONCURRENTLY" | "加监控" |

## 常见失分

1. 找到迁移锁就宣布根因，没解释 09:52 之后为什么没恢复（最常见、最致命）。
2. 把 `tn-orbit` 流量翻倍当根因（它时间上更早、数字更大），要求限流大客户。
3. 盯着 09:38 证书轮换（时间上最接近）。
4. 提议调大连接池或扩 task——不知道 `max_connections` 的账，也没注意 09:40 的 `remaining connection slots are reserved`。
5. 以为 `ALTER TABLE ADD COLUMN`（无默认值）本身很慢；正确说法是锁持有到事务结束。
6. 只看应用日志的 status：应用记 500（30 s 后），客户端看到的是 ALB 504（15 s）。

## 时间分配（30 min）

| 分钟 | 应完成 |
|---|---|
| 0–2 | 接班定框：两阶段假设、影响面、变更窗口 |
| 2–6 | ALB 信号拆分；p99 = 10 s 天花板 → 连接池；变更清单 |
| 6–12 | 阶段 A：迁移 + 锁 + 共享池 |
| 12–18 | 阶段 B：top SQL、缺索引、连回回滚；排除两个红鲱鱼 |
| 18–21 | 止血：关 flag + 连接账 + 验证 + 补索引计划 |
| 21–30 | 长期修复、postmortem 行动项、5 行 summary |
