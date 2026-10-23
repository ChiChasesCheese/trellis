# 子代理指令 · Abnormal onsite 练习（code review · incident · 旧流程去重题）

> 你是 `sonnet`（或 `opus`）子代理，**不得再派生代理**。只拥有分配给你的目录（和它对应的题解文章，若有），不碰别的文件。
> 读者 Chi：1.5 年后端（PayPal Braintree：Python/Kotlin、Snowflake/SQL、on-call 处理过真实事故），岗位 **Abnormal AI · SWE II – Insider Risk**（Identity Security 团队）。
> Abnormal 技术栈（官方工程博客，`../catalog/raw/official.md` O-17）：Python monorepo、Kafka、gRPC → Temporal、Postgres、OpenSearch、DynamoDB、Redis、AWS、Kubernetes。
> 证据：`../catalog/raw/process_and_rounds.md` §1.3–1.4、`../catalog/raw/questions_reported.md` Q8–Q16。**照原话出题，没原话的细节标 (reconstructed)**。

## 0. 先读

`../CONVENTIONS.md`（codebase 型目录与验收口径；code review 题沿用它）· `acceptance_conftest.py`（照抄，改 PACKAGE）。单文件题沿用 `../../millennium/CONVENTIONS.md` 与 `../../millennium/tasks/AGENT_PROBLEMS.md` §1 的硬规则（problem.md + starter_template.py + starter.py + solution.py + test_*.py + REPORT.md；kit 根 `conftest.py` 的 `impl` fixture）。

## 1. 恢复规则

开工先 `find <你的目录> -type f | head -100`；已存在且测试为绿的部分不重写，只补缺。

## 2. 通用硬规则

1. 只用标准库 + pytest。不联网。所有 IP 用文档网段（192.0.2.0/24、198.51.100.0/24、203.0.113.0/24），域名用 example.com/.org，人名虚构。
2. 学习者文字（`REVIEW_KEY.md`、`walkthrough.md`、`model_answer.md`、`rubric.md`、`followups.md`、`REPORT.md`）**中文**，技术名词英文括注；面试中要说出口的句子给**英文口播**。代码、注释、PR 描述、告警文本英文。
3. 所有数字来自你跑过的命令（行数 `wc -l`、测试数 `grep -c "def test"`、耗时）。不写过程话。
4. 完成后回复：目录树、验收命令最后一行、规模数字、你认为最弱的两处。

## 3. 分配

### A. `loop/rounds/03_code_review/cr01_alert_fanout/` + `cr02_risk_api/`（一个代理做两个）

原话（#8496901 Round 4）："I was given a small repository and asked to perform a code review. … Identify issues · Prioritize them (P0/P1/etc.) · Explain why certain issues were more important · Suggest concrete improvements. The second part involved extending the system and discussing how it would behave at larger scale … Concurrency · Parallelism · Worker scaling · Message queue scaling · Throughput · Bottlenecks · Failure scenarios … be prepared to go beyond 'add more workers' or 'use a queue.'" Glassdoor 2026-04："Code review & fix implementation with AI"。1p3a 2025-10："面试前有一个 link 给你预先 code review … 开始就讨论一下你的 comments，大概二十分钟换成 system design"。

每题目录：
```
PR.md            PR 描述（英文，像同事提的 PR：标题、动机、改了什么、"tested locally"）
starter/         小仓库 = PR 合入后的状态（600–1,000 行 Python，含少量测试，自带 pytest.ini，测试绿——bug 不被现有测试覆盖）
pr.diff          `diff -ruN` 从"PR 之前"到 starter 的补丁（PR 引入的部分；评审对象主要在 diff 里，但有 1–2 个问题在 diff 之外的既有代码里，考察是否看上下文）
solution/        修好 P0/P1 后的仓库（P2 可只在 REVIEW_KEY 里写）
acceptance/      每个 P0 至少一个测试、P1 至少半数有测试：starter 上 `core` 全红、solution 全绿；marker 用 `core`（P0）/`stretch`（P1）/`regression`
REVIEW_KEY.md    问题表：ID · 位置(file:line) · 优先级 P0/P1/P2 · 一句话问题 · 为什么是这个优先级（影响面 × 可能性 × 可发现性）· 具体修法 · 验收测试名。10–14 条：P0 3–4、P1 4–5、P2 3–5
walkthrough.md   45 min 怎么评：先读 PR.md 与 diff 的顺序；给 Claude 的评审提示词（"Review this diff for correctness under concurrency, failure modes, security and tenant isolation; cite file:line; rank by blast radius"）；如何复核 AI 的发现（AI 常见的假阳性/漏报）；评论的写法（英文示例 3 条：P0 一条、P1 一条、nit 一条）；口头总结模板（60 s，先 P0）
followups.md     第二部分"扩展 + 规模"：8–10 个追问，每个给中文要点 + 英文口播：吞吐估算（给数字自己算）、worker 扩容的上限（下游限流、DB 连接、分区数）、队列扩容（分区/分片与顺序性、可见性超时、DLQ、毒消息）、幂等键、背压、失败场景（下游宕机、重复投递、部分失败、重启）、观测（lag、age of oldest message）
REPORT.md        规模、问题分布、验收清单、每个 P0 的"为什么是 P0"
```
- **cr01_alert_fanout**（PR："Add notification fan-out worker for high-severity alerts"）：包 `fanout`。从队列（`queue.py`：sqlite 实现的 SQS 风格队列：`receive(max, visibility_timeout)`、`delete(receipt)`、`change_visibility`）取告警 → 查租户的通知配置（sqlite）→ 去重 → 按渠道（webhook、email stub、Slack stub）发送，`ThreadPoolExecutor` 并发，重试。埋点建议（可调整，但 P0 要真能被测试证明）：**P0** 先 `delete` 再处理（崩溃丢消息）· 去重缓存是多线程共享 dict 且 key 不含 tenant（竞态 + 跨租户吞通知）· 重试无上限无退避、无 DLQ（毒消息热循环）· 租户配置查询字符串拼 SQL（注入）；**P1** webhook 请求无超时 · 日志打印 webhook secret · `except Exception: pass` 吞错 · naive datetime 比较窗口 · 每条消息 N+1 查配置；**P2** 魔法数字、可变默认参数、缺失败路径测试、函数过长。
- **cr02_risk_api**（PR："Add per-user risk score endpoint with caching"）：包 `riskapi`。标准库 WSGI 小服务：`GET /tenants/<t>/users/<u>/risk`、`GET /tenants/<t>/users?sort=&cursor=`，API key 认证，Redis 风格缓存（`cache.py` 内存实现，带 TTL）。埋点建议：**P0** IDOR（只校验 key 有效，不校验 key 的租户 == 路径租户）· `sort` 参数拼进 SQL ORDER BY（注入）· 缓存值用 `pickle` 反序列化（缓存被投毒即 RCE；改 json）· API key 用 `==` 比较且存明文/MD5（时序 + 泄露）；**P1** 缓存 key 不含 tenant · 缓存击穿（热点 key 过期时并发全打 DB，无 single-flight）· 分页 off-by-one（cursor 用 `>=` 重复一条）· 无 limit 上限（一次拉全表）· 日志含 PII（email）；**P2** 命名、重复代码、缺类型、错误形状不统一。

### B. `loop/rounds/02_incident_sd/ic01_ingest_lag/` + `ic02_api_5xx/`（一个代理做两个）

原话（#8496901 Round 3）："I was given access to an AWS environment and had to investigate an incident. The goal was to figure out: What was going wrong · How I would identify the root cause · What signals/logs/monitoring tools I would look at · What the immediate mitigation should be · What long-term fixes I would recommend. The interviewer was interested not just in finding the issue, but also in how I approached debugging and how I prioritized short-term mitigation vs. long-term remediation."（#8387564："started with a production incident that I had to investigate and resolve"）。

真实面试给的是 AWS 控制台。我们造一个**可查询的离线 AWS 快照** + 一个模仿 AWS CLI 形状的查询工具，让 Chi 练"先看什么、怎么缩小范围、怎么说"。每题目录：
```
PAGE.md          你被 page 时看到的告警（英文，2–4 行：告警名、指标、阈值、开始时间）+ 一句"you have console access; walk us through it"
env/             快照：cloudwatch/metrics/<namespace>/<metric>.csv（时间,值,维度）· cloudwatch/logs/<log-group>/<stream>.jsonl · cloudtrail/events.jsonl · deploys.json（ECS/K8s 部署历史含镜像 tag 与 commit message）· config/（变更前后的配置）· 资源描述（sqs/msk/rds/dynamodb 的 describe 输出 JSON）
awsim.py         查询 CLI（标准库）：`python3 awsim.py metrics list|get --namespace N --name M [--dim k=v] --start --end --stat Average|Sum|Maximum|p99 --period 60` · `logs groups|tail|filter --group G --pattern "ERROR" --start --end` · `logs insights --group G --query "fields ... | filter ... | stats count() by bin(1m)"`（支持一个够用的小子集：fields / filter 含 like 与比较 / stats count/avg/max by 字段或 bin / sort / limit）· `trail lookup --event-name X` · `deploys` · `describe <resource>`；输出像 AWS CLI 的 JSON/表格
tests/           awsim 的测试（查询子集正确）+ `test_story.py`：断言根因证据在快照里确实存在（例：部署时间点之后某错误率从 ~0 升到 > X%），保证题目自洽
investigation.md 推荐的排查路径（中文 + 英文口播）：前 2 分钟问什么（影响面、开始时间、最近变更）→ 看哪些图 → 怎么用 logs insights 缩小 → 如何确认根因（反事实：为什么不是红鲱鱼）→ 立即止血的选项与取舍（rollback / feature flag / scale / throttle，各自风险）→ 长期修复（代码、容量、告警、runbook、测试）→ 写一段 5 行的 incident summary
model_answer.md  时间线（UTC，分钟级）+ 根因 + 每条结论引用的证据（awsim 命令 + 输出要点）+ 止血 + 长期修复 + postmortem 行动项
rubric.md        strong / ok / weak：调试方法（假设驱动 vs 乱翻）、止血优先于根因、红鲱鱼处理、沟通（状态更新）、长期修复的质量
REPORT.md        快照规模、红鲱鱼清单、awsim 支持的查询、测试数
```
- **ic01_ingest_lag**：告警 "alert-ingest consumer lag > 50k for 10 min"。系统：MSK(Kafka) topic `security-events` → ECS 服务 `alert-ingest`（8 tasks）→ enrichment 调内部 `geoip-svc` → 写 Postgres。根因（reconstructed）：14:02 的部署把 geo-ip 查询从批量 + 本地缓存改成每条同步调用（commit message 说 "simplify geoip client"）；`geoip-svc` 开始返回 429（限流），客户端无退避地立即重试 → 每条消息耗时从 ~3 ms 到 ~400 ms，消费速率崩，lag 线性增长；DLQ 开始有消息。红鲱鱼：同时段另一服务 CPU 告警；RDS CPU 正常；一个 broker 的磁盘告警早于事件一小时且已恢复。止血取舍：扩 consumer 无效甚至更糟（更多 429，且受 partition 数上限）→ 回滚部署是对的；长期：客户端缓存 + 批量 + 带抖动的指数退避 + 熔断、对 429 的告警、消费吞吐 SLO、部署的 canary 指标门禁。
- **ic02_api_5xx**：告警 "portal-api 5xx rate > 5% and p99 > 3 s"。系统：ALB → ECS `portal-api`（连接池 20/task）→ RDS Postgres。根因（reconstructed）：09:40 一个迁移（CloudTrail 与部署记录可见）在大表 `alerts` 上加带默认值的列 / 建索引没用 `CONCURRENTLY`，持有锁；查询排队 → 连接池耗尽 → ALB 504/503；之后锁释放但一个新端点的查询没走索引（缺失的索引正是那次迁移本该建的），RDS `DatabaseConnections` 打满、`ReadIOPS` 高，p99 一直高。红鲱鱼：同时段证书轮换事件（CloudTrail）；一个租户流量翻倍（是放大器不是根因）。止血：终止阻塞的迁移会话 / 回滚端点 feature flag / 临时提高池上限的风险；长期：迁移规范（`CONCURRENTLY`、分批回填、lock_timeout）、慢查询告警、按租户限流、连接池与 RDS max_connections 的容量模型。

### C. `loop/rounds/06_legacy_coding/pc01_image_dedup/`（单文件题，一个代理；可与别的小任务合并）

原话（1p3a 1059585 / 1072363 / 1074077 / 1137132 摘要，2024-04 → 2025-07，"20 分钟讨论 + 30 分钟写"）："给你一堆图片 找出 duplicate 的图片 如果 memory 有限 怎么做 如果要 hashing 怎样做 如果有 hashing collision…"；"写出 main function，我写的 python，给了 os.walk 的用法提示，直接 call 他给的 `_calculate_hash` 会有 hash collision，问解决方法，最后问 system design"；"如果你的 file system 里面有很多照片，如何删除重复的照片"。PracHub 2025-07："Design a duplicate-file removal algorithm" / "Design a scalable photo deduplication service"。
- Part 1：`find_duplicates(root) -> list[list[str]]`：`os.walk`，先按文件大小分桶，再对同大小文件分块（`chunk_size`）流式哈希；输出组内按路径排序、组按首路径排序；空文件、符号链接（不跟随）、不可读文件（跳过并计数）。
- Part 2：给定的 `_calculate_hash` 是**故意弱的**（如只哈希前 1 KB + 文件大小，或 32 位截断）——哈希相同后用逐块字节比较确认，处理碰撞；测试构造真碰撞。
- Part 3 **(reconstructed)**：`plan_deletions(groups, policy)` 选保留哪一个（最早 mtime / 最短路径 / 指定目录优先），返回要删的列表，`dry_run` 默认 True；以及近似重复（视觉相同但字节不同）：输入给 8×8 灰度矩阵（不依赖 PIL），实现 average hash + 汉明距离阈值分组（只讲 + 小实现）。
- `problem.md` 的追问与 §SD：内存受限、海量文件（分布式：按大小/前缀哈希分片、MapReduce 式两阶段）、对象存储（S3 ETag 不等于内容哈希的坑）、照片去重服务（上传时 perceptual hash + 近邻索引）。
- 测试用 `tmp_path` 建文件；`perf`：2 万个小文件 + 若干大文件 < 2 s。题解文章 `study/30-articles/pc01_image_dedup.md`（模板 `../../millennium/study/30-articles/_TEMPLATE.md`）。

## 4. 若 Write 工具拒绝写 `REPORT.md`

子代理环境可能拒绝写名为 REPORT 的文件。**不要绕过**：把 REPORT.md 的完整内容放在最终回复里（标题 `## REPORT.md`），编排者保存。
