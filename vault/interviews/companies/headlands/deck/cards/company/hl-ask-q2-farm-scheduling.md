---
id: hl-ask-q2-farm-scheduling
node: company.questions-to-ask
type: qa
step: 3
---
## Q
反问面试官："计算集群如何调度和失败"，英文怎么问？为什么好，好 / 坏答案各透露什么？

## A
> "When a researcher submits a big batch of jobs to the compute farm, how is it scheduled, and what happens when a node dies halfway — is that custom code or built on open-source pieces?"

- **为什么好**：JD 的词是 distributed computing farm 和 open-source libraries；同时问**自研 vs 开源**与**失败语义**，这是分布式系统里最能区分经验的两点。
- **好答案**：有清晰的重试 / 幂等 / 调度策略；说得出哪部分自研、为什么；承认某些地方是技术债。
- **坏答案**："研究员自己重跑"（没有可靠性设计，你会被叫去救火）；或一律"都是自研的"却说不出理由。
