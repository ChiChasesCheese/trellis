---
id: infra-k8s-primitives
node: infra.containers
type: qa
---
## Q
At design-conversation depth: what do a Kubernetes Pod, Deployment, Service, and HPA each abstract?

## A
- **Pod**: smallest schedulable unit — one or more containers sharing network and storage. Mortal by design; its IP is ephemeral.
- **Deployment**: a declared desired state ("N replicas of image X"); a controller continuously reconciles reality toward it — that reconciliation loop is what gives self-healing and rolling updates.
- **Service**: a stable virtual IP/DNS name load-balancing over whichever pods are currently healthy — the answer to "pods die and change IPs".
- **HPA** (horizontal pod autoscaler): adjusts replica count to hold a metric at a target (e.g. 70% of requested CPU). It's reactive — scrape interval plus pod boot time means it lags spikes, so it can't replace headroom.

## Q zh
在设计对话深度：什么 Kubernetes Pod、Deployment、Service 和 HPA 各抽象？

## A zh
- **Pod**：最小可调度单元——一个或多个容器共享网络和存储。按设计必死；它的 IP 是短暂的。
- **Deployment**：声明的期望状态（"N 个副本的镜像 X"）；一个控制器连续协调现实向它——那个协调循环就是给自愈和滚动更新的东西。
- **Service**：一个稳定的虚拟 IP/DNS 名称负载均衡在无论当前健康的哪些 pod——"pod 死亡和改变 IP"的答案。
- **HPA**（水平 pod 自动扩展器）：调整副本计数以保持指标在目标（例如请求 CPU 的 70%）。它是反应性的——刮取间隔加 pod 启动时间意味着它滞后尖刺，所以它不能替代余量。
