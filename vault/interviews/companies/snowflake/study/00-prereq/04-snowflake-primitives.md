# 前置课 04 · 用你自己的 Snowglobe 经验讲 Snowflake 原语

> 目标：把两年重度使用的经验变成面试里可引用的"我做过 + 它背后是什么"。读完能在任何 SD / expertise 追问里，30 秒内从自己的系统跳到 Snowflake 的对应机制。素材：`../../../../core/stories/evidence-base.md` S1/S2/S5/S7、`../20-cards/snowflake_internals.md`。

## 1. 你用过的 → 它背后是什么 → 面试怎么说

| 你在 Snowglobe 做的 | 背后的原语 | 一句话桥 |
|---|---|---|
| 6 条 append-only stream 按 record type 分流 GRRCN 文件 | Stream = 表版本 offset 书签；append-only 只看 INSERT | "I fan out by record type with append-only streams; the offset only advances inside the MERGE transaction, so a failed task replays instead of losing rows." |
| `WHEN SYSTEM$STREAM_HAS_DATA()` 门控的 task DAG | Task graph；serverless vs 自管仓库；`SUSPEND_TASK_AFTER_NUM_FAILURES` | "Nothing runs on empty input; a failing branch suspends itself rather than poisoning the DAG." |
| feature-flag 急停 `AGGREGATED_AMEX_SEPARATE_FLOW` | 配置表驱动的 task 条件；灰度 | "One flag stops the whole flow; rollout is merchant-by-merchant behind a toggle." |
| MERGE 键幂等 | 事务性 MERGE + 不可变 micro-partition | "Every stage is an upsert on natural keys; re-running is a no-op." |
| shadow-run 对账 13.7M 行 / 0.224% | Time Travel + clone 做对照环境 | "I cloned the target, ran both sources, diffed at day level, and only then flipped." |
| snowglobe-tools schema pool（多 agent 并行不撞 DDL） | zero-copy clone 是元数据操作 | "Clones are metadata pointers, so an isolated schema per branch costs nothing." |
| Terraform 管 grants；`GRANT OWNERSHIP` 被拒 7 分钟 RCA | RBAC 是 DAG（role 继承）；ownership 与 outbound privileges | "Snowflake's RBAC is a DAG with deny-less inheritance — which is exactly the pc01 phone-screen problem." |
| Streamlit task monitor + Datadog 告警 | `TASK_HISTORY()`、`QUERY_HISTORY` | "Observability of streams/tasks is the thing I'd improve as a user — I built it myself." |

## 2. 被追问时的三层

**why**：为什么选 Snowflake-native 编排而不是 Airflow？——数据不出仓、每步是事务 MERGE、运维简单；代价是可观测性弱。
**alternatives**：Airflow + 外部解析服务（弃：数据出仓、双写一致性）；Ruby 脚本续命（弃：无法做 EU 扩展与幂等）。
**now**：会把下游聚合改成 Dynamic Tables（TARGET_LAG，自动增量）；质量门从第一天做商户粒度。

## 3. 三个能反问的真问题

1. Stream staleness 为什么是静默的？有没有"即将过期"的信号？（对应 Streams 保留期自动延长到 14 天）
2. Task DAG 里下游失败是独立重试还是整个 DAG 重跑？（对应 sd02 / od05 的部分失败语义）
3. Adaptive Refresh 用什么信号决定重初始化？（对应 sd08）

## 4. 自测

- [ ] 不看卡，30 秒说出 Stream offset 推进的条件与后果
- [ ] 30 秒说出 Execution Anchor 的两种转移
- [ ] 用自己的 S1 讲一遍"幂等 + 急停 + 对账"三件套，带数字
