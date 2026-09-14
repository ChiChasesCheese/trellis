---
id: architecture-when-to-split
node: architecture.services
type: qa
---
## Q
What are legitimate triggers for splitting a monolith into services — and what is the default recommendation for a new system in 2026?

## A
Legitimate triggers (organizational and operational, not aesthetic):
- **Team scaling**: deploy trains and merge conflicts across many teams; you split so teams can ship independently (Conway alignment).
- **Divergent scaling/runtime needs**: one component needs 50x the instances, a different language, or isolation for a risky dependency.
- **Fault isolation** for a component whose failure must not take the core down.

Default for new systems: a **modular monolith** — enforced module boundaries in one deployable. You get boundary discipline without the distributed-systems tax, and clean modules are the extraction seams if a real trigger arrives. "Microservices for scale" alone is not a trigger; monoliths scale horizontally fine.

## Q zh
将整体分裂成服务的合法触发器是什么——2026 年新系统的默认建议是什么？

## A zh
合法触发器（组织和操作，不是美学）：
- **团队缩放**：部署火车和跨许多团队的合并冲突；你分裂所以团队可以独立船（Conway 对齐）。
- **发散的缩放/运行时需求**：一个组件需要 50 倍实例、不同语言或隔离为有风险的依赖。
- **故障隔离**对一个组件其故障不能击倒核心。

新系统的默认：一个**模块化整体** ——在一个可部署中强制的模块边界。你获得边界纪律而不分布式系统税，干净模块是提取接缝如果真实触发器到达。"微服务对缩放"单独不是触发器；整体缩放水平很好。
