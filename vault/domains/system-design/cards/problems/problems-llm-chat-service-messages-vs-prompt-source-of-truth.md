---
id: problems-llm-chat-service-messages-vs-prompt-source-of-truth
node: problems.realtime.llm-chat-service
type: qa
step: 2
tags: [grown]
---
## Q
In a multi-turn chat service backend, why should the raw, per-turn messages be stored as the only authoritative data, with the actual prompt sent to the model on each turn treated as a disposable value recomputed at request time — rather than storing the assembled prompt itself as the record of what happened?

## A
The assembled prompt depends on a policy that changes over time: how much context window budget is available, how older turns get truncated or summarized, and which model is serving the conversation. If the assembled prompt were stored as the authoritative record, upgrading the model (a different context window size) or changing the summarization policy would leave historical records built under a stale policy with no way to regenerate them under the new one. Keeping raw messages as the only source of truth and rebuilding the prompt fresh on every turn means a policy or model change only requires changing the assembly logic, not migrating stored data.

## Q zh
在一个多轮对话服务的后端里，为什么应该把每一轮的原始消息存储为唯一权威数据，把每一轮实际发给模型的 prompt 当作运行时重新计算出的一次性派生值——而不是把拼装好的 prompt 本身当作「发生过什么」的记录存起来？

## A zh
拼装出的 prompt 依赖一套会随时间变化的策略：有多少上下文窗口预算可用、更早的轮次如何被截断或摘要、以及当前是哪个模型在服务这个会话。如果把拼装好的 prompt 当作权威记录存起来，一旦升级模型（上下文窗口大小变了）或调整摘要策略，历史记录里存的就是在旧策略下构建的产物，无法用新策略重新生成。只把原始消息当作唯一权威数据、每一轮都动态重新拼装 prompt，意味着策略或模型的变化只需要改拼装逻辑，不需要迁移存量数据。
