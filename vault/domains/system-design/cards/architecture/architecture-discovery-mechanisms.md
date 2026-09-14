---
id: architecture-discovery-mechanisms
node: architecture.discovery
type: qa
---
## Q
Client-side vs server-side service discovery: how does each find healthy instances, and which does Kubernetes give you?

## A
- **Client-side**: caller queries a registry (Consul, Eureka) and load-balances across instances itself. Fewer hops and smart per-request balancing, but discovery logic lives in every client/language.
- **Server-side**: caller hits a stable virtual name; a load balancer/proxy resolves to instances. Dumb clients, but an extra hop and the LB is now critical infra.
- **Kubernetes**: server-side by default — a `Service` gives a stable DNS name/VIP; readiness probes gate which pods receive traffic. A service mesh (sidecar or ambient) moves balancing back client-side without app code.

Either way, the registry's real job is **health**: instances are registered on start and evicted on failed health checks/missed heartbeats — a registry of dead instances is worse than none.

## Q zh
客户端服务发现 vs 服务器端服务发现：每个如何发现健康实例，Kubernetes 给你什么？

## A zh
- **客户端**：调用者查询一个注册表（Consul、Eureka）并自己跨实例负载均衡。更少 hop 和聪明的每请求平衡，但发现逻辑在每个客户端/语言。
- **服务器端**：调用者击中稳定虚拟名字；负载均衡器/代理解析为实例。哑客户端，但额外 hop 和 LB 现在是关键基础设施。
- **Kubernetes**：默认服务器端——一个`Service`给出稳定 DNS 名字/VIP；就绪探针门哪个 pod 接收流量。服务网格（sidecar 或环境）移动平衡回客户端无应用代码。

无论如何，注册表的真实工作是**健康**：实例在启动时注册并在故障健康检查/错过心跳时驱逐——死实例的注册表比没有更差。
