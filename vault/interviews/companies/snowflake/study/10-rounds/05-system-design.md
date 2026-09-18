# 05 · 系统设计（45–60 min，infra / data 题）

> 本轮全部题目（含 GitHub 蒸馏补充的新题，按 28 法则排序）：[`../../CONTENTS.md`](../../CONTENTS.md) §05_system_design。本文件里点名的题是示例，不是全集。

> 事实层在 `../../loop/LOOP_GUIDE.md` §6；题目证据 `../../catalog/raw/system_design.md`；口述卡 `../20-cards/sd_checklist.md`。本章：**怎么练**。

## 这轮到底考什么（一句话）

**不变量 → API/数据模型 → 失败模式，而且题目是 Snowflake 自己在建的那类系统。** KV store、调度器、队列、配额、审计日志、物化视图缓存——候选人原话"更接近 data-platform 问题，不像标准的'设计一个 web 服务'"。

两个一手风险：**面试官全程沉默**（IC1/IC2，"SQL engine as cron job"）；**onsite 每轮都要 Hire**。

## 练法：每题 45 分钟，三遍

1. **第一遍（开卷）**：读 `prompt.md` → 自己口述 45 分钟（录音）→ 对 `rubric.md` 五维自评 → 读 `model_answer.md` 找差距。
2. **第二遍（闭卷）**：只看 `prompt.md` 和 `sd_checklist.md`，再讲一遍；`followups.md` 让人或自己抽 4 条，每条 60 秒。
3. **第三遍（沉默面试官）**：计时器开着，全程不看任何材料，每 5 分钟自己说一句"我现在在做 X，接下来 Y"。

```bash
cd vault/interviews/companies/snowflake
python3 loop/mock.py start sd02 -m 45    # 打印 prompt，开始计时
python3 loop/mock.py time sd02
```

## 必做题（28 法则顺序）

| 顺序 | 题 | 一句话核心 | 一手追问 |
|---|---|---|---|
| 1 | **sd01 KV Store** | 不可变块 + 元数据版本 = time travel；单分区 Raft；跨分区 2PC | — |
| 2 | **sd02 Cron / Job Scheduler** | 唯一约束插 run + CAS 认领 + 租约兜底；at-least-once | — |
| 3 | **sd03 SQL Notebook** | submit → poll → fetch；大结果分片流式；排队 | ✔ |
| 4 | sd04 Quota | 强一致中心计数 vs 本地预分配 + 定期对账 | ✔ |
| 5 | sd06 Audit Log | 追加写 + 哈希链防篡改；时间窗倒排；保留 | — |
| 6 | sd07 Rate Limiter | token bucket vs 滑窗；Redis Lua 原子；多规则叠加 | ✔ |
| 7 | sd05 Distributed Queue | 落盘再 ack；visibility timeout；背压 | ✔ |
| 8 | sd11 Jira → PR 自动化 | 异步任务流水线；幂等；人审门；LLM 步骤失败 | — |
| 9 | sd08 DAG MV Cache | 依赖图；增量 vs 全量；一致快照 ≈ Dynamic Tables | — |
| 10 | sd09 Password Storage | argon2/bcrypt 参数、盐、pepper、轮换 | — |
| 11 | sd10 Web Crawler | 去重、礼貌性、分片 | — |

## 差异化：用 Snowflake 自己的原语作参照

早期职业候选人最便宜的加分，就是在对的地方说一句：
- 调度器 / 单写者 → **Execution Anchor**（每个查询绑定恰好一个 GS 实例，绑定存 FDB）
- 消费者幂等 → **Streams offset 只在 DML 事务内推进**
- 物化视图缓存 → **Dynamic Tables** 的增量 / 重初始化判定
- 快照 / 版本 → **micro-partition 不可变 + FDB 版本列表**（clone 与 time travel 都是元数据操作）

细节：`../20-cards/snowflake_internals.md`、`../00-prereq/04-snowflake-primitives.md`。

## 你自己的素材怎么进 SD

- sd02 调度器 ↔ [[S1]] 的 task DAG + `STREAM_HAS_DATA` 门控 + 急停 flag
- sd05 队列 ↔ intern 的 Kafka→Snowflake connector（poison message 隔离）
- sd06 审计 ↔ [[S2]] quality-check 的不可变结果表
- sd08 MV cache ↔ [[S5]] shadow-run（增量对账 vs 全量重算的取舍）

一句"我在 Braintree 做过这件事的一个版本"，比十句教科书更能拿 4 分。

## 挂点 → 对策

| 挂点 | 对策 |
|---|---|
| 直接画框 | 前 4 分钟只说不变量与"不做什么" |
| 说能 exactly-once | at-least-once + 消费方幂等键 |
| 沉默面试官下停住 | 自问自答："A natural follow-up is X; my answer is…" |
| 没有数字 | 超时、退避序列、租约时长、分片数，每个组件至少一个数 |
| 画完就停 | 最后 5 分钟讲 rollout / 监控 / 怎么验证正确（shadow-run） |
