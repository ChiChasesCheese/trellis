---
id: nr-amz-s11-followups
node: amazon.s11
type: qa
step: 3
---
## Q
【S11 · 实习期：Kafka 事件流 · Spring · Spark（广度补充）】面试官会追问什么？每个怎么答？

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
