# 卡片 · 系统设计 45 分钟口述检查卡（Snowflake 版）

> 依据：`../../loop/LOOP_GUIDE.md` §6、Stripe sd rubric 五维、`../../catalog/raw/system_design.md` §2 风格画像（面试官两极：多数给 hint，至少一例全程沉默）。**沉默面试官下，这张卡就是你的面试官。**

## 时间表（45 min）

| 分钟 | 做什么 | 说出口的句子 |
|---|---|---|
| 0–4 | 两句话复述 + **不变量**（3–4 条）+ 明确"不做什么" | "Let me restate: … The invariants I'll design around are … I'm explicitly not promising …" |
| 4–8 | 规模与约束：QPS、数据量、延迟目标、一致性要求、多租户 | "I'll assume ~X/s and Y TB; tell me if that's off." |
| 8–15 | **API 契约 + 数据模型**（先于框图）：调用方是谁、幂等键、版本、分页 | "Before boxes: the write path is …, keyed by …, idempotent on …" |
| 15–25 | 核心流程：一次写、一次读、一次失败重试各走一遍 | "A request enters at …; on crash here we …" |
| 25–35 | **失败模式与规模**：热点、噪声邻居、重试风暴、分区、副本一致性 | "The thing that breaks first is …; I'd isolate it by …" |
| 35–40 | 分层与组件；rollout / 监控 / 测试 | "Stateless workers here, the only stateful part is …; I'd page on …" |
| 40–45 | 用 Snowflake 原语作参照 + 反问 | "This is the same shape as your Execution Anchor / Dynamic Tables …" |

## 每题必答的五问（rubric 五维）

| 维 | 自问 | 4 分的样子 |
|---|---|---|
| Problem framing | 不变量说了吗？"不做什么"说了吗？ | 至少一条不变量是**否定式**（不保证顺序 / 不承诺 exactly-once） |
| API & data model | 幂等键是什么？谁去重？版本怎么表达？ | 每张表说清主键与不可变性；每个 API 说清重试语义 |
| Failure modes & scale | 先坏哪里？租户隔离？重试风暴？ | 具体数字（超时、退避、上限、DLQ）而非"加重试" |
| Separation of concerns | 慢路径（配置/匹配）与快路径（执行）分开了吗？ | 无状态 worker + 唯一有状态组件点名 |
| Delivery | 怎么灰度？page 什么？怎么验证正确？ | shadow-run / 对账 / feature flag（S5 的真实做法） |

## Snowflake 味的三个加分句

1. **单写者**："I'd bind each job to exactly one scheduler instance with a lease in the metadata store — that's what your Execution Anchor does for queries."
2. **增量 vs 全量**："The cache invalidation is a dependency DAG; incremental when the upstream delta is small, reinitialize when it isn't — the Dynamic Tables adaptive-refresh decision."
3. **offset 只在事务内推进**："Consumers advance the offset in the same transaction as the write, so a crash replays instead of skipping — Streams semantics."

## 反例（一句话识别弱答案）

- "加缓存、加队列、加机器" 而没说**哪个组件有状态**。
- 说能做到端到端 exactly-once。
- quota / rate limiter 说不清**强一致 vs 本地缓存 + 同步**的代价。
- 调度器不谈**双触发**（多副本）与**漏触发**（崩溃）。
- 审计日志不谈**不可变**与**保留策略**。
