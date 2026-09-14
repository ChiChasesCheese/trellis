---
id: infra-mesh-tax-ambient
node: infra.mesh
type: qa
---
## Q
What does a sidecar mesh cost in latency and operations, and how does the ambient/sidecarless model restructure that cost?

## A
- **Latency tax**: two extra proxy traversals per hop (caller's sidecar out, callee's sidecar in), roughly **0.5–2 ms at p99 per hop** — compounding across deep call chains.
- **Ops tax**: one proxy per pod (CPU/memory × every pod), proxy upgrades coupled to pod restarts, and one more layer in every debugging session.
- **Ambient** (e.g. Istio ambient mode) splits the proxy: a shared **per-node L4 tunnel** provides mTLS and telemetry with no per-pod sidecar, and optional **L7 waypoint proxies** are deployed only for services that need HTTP-level policy. You pay the L7 tax only on routes that use it.

## Q zh
一个 sidecar 网格成本什么在延迟和操作，ambient/sidecarless 模型如何重建那个成本？

## A zh
- **延迟税**：每跳两个额外 proxy 遍历（调用者 sidecar 出、被调用者 sidecar 入），大约**每跳 p99 0.5–2 毫秒**——通过深调用链复合。
- **操作税**：每 pod 一个 proxy（CPU/内存 × 每 pod），proxy 升级耦合到 pod 重启，每个调试会话多一层。
- **Ambient**（例如 Istio ambient 模式）分裂 proxy：共享的**每节点 L4 隧道**提供 mTLS 和遥测无需每 pod sidecar，和可选**L7 waypoint proxy** 仅为需要 HTTP 级别策略的服务部署。你仅在使用它的路由上付 L7 税。
