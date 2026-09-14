---
id: foundations-three-pillars
node: foundations.tradeoffs
type: qa
---
## Q
DDIA judges every data system against three nonfunctional pillars. Name them, and give the operational test you would apply to a running system for each — the question that reveals whether the pillar actually holds.

## A
- **Reliability** — the system keeps doing the right thing when things go wrong: hardware faults, software bugs, human error. Test: *kill a node, ship a bad config — does the fault stay contained, or does it become a user-visible failure?*
- **Scalability** — not "it scales", but a concrete plan for growth: load is described with measurable load parameters (QPS, fan-out, working set…), and you know which resource saturates first. Test: *"if load went 10×, what breaks first and what is the prepared next step?"*
- **Maintainability** — the majority of cost arrives after launch: future engineers must be able to operate, understand, and change the system. Test: *how painful is a deploy, a schema migration, an on-call shift?*

They are requirements to negotiate per system, not virtues — e.g. a batch pipeline may trade tail latency for throughput, a prototype may trade evolvability for speed.

## Q zh
DDIA 用三个非功能性支柱来评判每个数据系统。说出它们，并为每个支柱给出你会对一个运行中系统做的操作性检验 — 即那个能揭示该支柱是否真正成立的问题。

## A zh
- **可靠性（Reliability）** — 出问题时系统仍然做正确的事：硬件故障、软件 bug、人为失误。检验：*杀掉一个节点、上线一个坏配置 — 故障（fault）是被控制住了，还是升级成了用户可见的 failure？*
- **可扩展性（Scalability）** — 不是一句"它能扩展"，而是应对增长的具体计划：用可度量的负载参数（load parameters，如 QPS、扇出、工作集大小……）描述负载，并且你知道哪个资源会最先饱和。检验：*"如果负载变成 10 倍，最先坏的是什么，准备好的下一步是什么？"*
- **可维护性（Maintainability）** — 大部分成本发生在上线之后：未来的工程师必须能运维、理解并修改这个系统。检验：*一次部署、一次 schema 迁移、一轮 on-call 有多痛苦？*

它们是需要按系统逐个权衡的需求，而不是美德 — 例如批处理管道可以用尾延迟换吞吐，原型可以用可演化性换速度。
