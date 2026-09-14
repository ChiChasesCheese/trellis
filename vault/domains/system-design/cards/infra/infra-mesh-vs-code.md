---
id: infra-mesh-vs-code
node: infra.mesh
type: qa
---
## Q
mTLS, retries, and traffic splitting can live in a shared library or in the mesh. When does the mesh win, and what does it inherently do worse than code?

## A
- Mesh wins on **polyglot fleets** (one proxy implementation vs a library per language), **upgrades without redeploying apps**, and **uniform enforcement** — security can guarantee mTLS everywhere without trusting every team.
- Code wins on **context**: the app knows which calls are idempotent and what a sensible fallback is. A mesh retry policy applies blindly per route — it can retry non-idempotent writes, and it can stack with app-level retries into a multiplicative retry storm.
- Working split: transport concerns (mTLS, telemetry, routing, splitting) to the mesh; semantic concerns (fallbacks, idempotency-aware retries, business timeouts) in code — and configure retries at **exactly one** layer.

## Q zh
mTLS、重试、流量分割可以住在共享库或网格。网格何时胜出，什么它本身比代码做得更差？

## A zh
- 网格在**polyglot fleet** 胜出（一个 proxy 实现 vs 每种语言的库），**无需重新部署应用的升级**，和**统一强制**——安全可以保证 mTLS 到处没有信任每个团队。
- 代码在**上下文**胜出：应用知道哪些调用是幂等的以及什么是合理的回退。网格重试策略按每个路由盲目应用——它可以重试非幂等写，它可以与应用级重试堆积成乘法重试风暴。
- 工作分裂：运输关注（mTLS、遥测、路由、分割）到网格；语义关注（回退、幂等感知重试、业务超时）在代码——并在**恰好一个**层配置重试。
