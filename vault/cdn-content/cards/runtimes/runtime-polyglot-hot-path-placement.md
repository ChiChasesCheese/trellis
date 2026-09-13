---
id: runtime-polyglot-hot-path-placement
node: runtimes.polyglot
type: qa
---
## Q
A team wants to put complex personalization logic in edge Lua because it avoids a network hop. What decision test should stop a bad hot-path placement?

## A
Keep edge logic small, deterministic, bounded, and safe under every request. Put parsing/routing primitives close to the proxy only when they need local phase data and can run without blocking; move rapidly changing business rules, heavy computation, durable state, and large dependencies to a service or build-time artifact. Judge total tail latency, failure blast radius, rollout/debuggability, and ownership—not only the saved hop.

## Q zh
团队想把复杂 personalization logic 放进 edge Lua，因为能省一个 network hop。什么 decision test 能阻止错误的 hot-path placement？

## A zh
edge logic 应保持小、deterministic、bounded，并对每个请求都安全。只有当 parsing/routing primitive 需要本地 phase data 且不会 blocking 时，才放在 proxy 附近；快速变化的 business rule、heavy computation、durable state 和大型 dependency 应移到服务或 build-time artifact。判断依据是整体 tail latency、failure blast radius、rollout/debuggability 与 ownership，而不只是省掉一次 hop。
