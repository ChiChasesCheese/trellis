---
id: nr-amz-s11-followups
node: amazon.followups
type: qa
step: 51
---
## Q
<p class="title">实习：Kafka 事件流<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

## A
- **How do you not double-charge / not miss fees?**
    - **At-least-once + 消费者幂等**；**批内先去重再插入**；**唯一约束**兜底竞态
    - 捕获 **`DataIntegrityViolationException`** 跳过；**`BatchListenerFailedException`** 精确重投失败那条
- **How does Connect scale?**
    - **replicas × `tasks.max`**，上限 **partition 数**；吞吐不够先看 partition 数
- **What's the Kafka proxy?**
    - broker 前面的代理：**SASL SCRAM + 双向 TLS**，凭据走 **vault**；不是 egress proxy
    - broker/proxy 归平台团队；我做的是**消费 / 落地 / 校验**
- **Proto → table?**
    - **自定义 converter → JSON → Snowflake schematization** 展开列；坏消息返回 **NULL**
- **Real-time vs batch?**
    - **实时**（Kafka + Connect，秒级）搬数据、算费用；**批**（Spark + Airflow，每日）事后校验
- **What if a consumer crashes?**
    - 短间隔 auto-commit 偏 **at-most-once**；真正的保护是**上游重试 + 对账 / 健康检查**
- **What did the Spark validators check?**
    - **定价计划创建来源**和**结算数据合规**；结果发 **Slack**

<div class="sources"><b>表达 · business English</b><br>• <b><i>dedup before insert</i></b> — 插入前先去重<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The consumer does dedup before insert and relies on a unique constraint for races.”</span><br>• <b><i>capped by partitions</i></b> — 被 partition 数封顶<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Parallelism is replicas times tasks, capped by partitions.”</span><br>• <b><i>defense in depth</i></b> — 多层防护<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Idempotency has three layers, which is defense in depth.”</span></div>
