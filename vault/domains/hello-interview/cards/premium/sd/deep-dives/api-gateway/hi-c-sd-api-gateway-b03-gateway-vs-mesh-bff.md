---
id: hi-c-sd-api-gateway-b03-gateway-vs-mesh-bff
node: sd.deep-dives.api-gateway.beyond
type: qa
step: 3
---
## Q
**API 网关 · 网关、服务网格与 BFF 的分工**｜拓展 · 加分

API 网关、服务网格（service mesh）和 BFF（Backend for Frontend）都在服务前面加一层，各自管什么？

## A
- **API 网关管南北向：** 外部客户端进到系统内部的流量（north-south），关心路由、对外鉴权、限流。
- **服务网格管东西向：** 服务之间互相调用的流量（east-west），用每个服务旁边的代理（sidecar）统一做 mTLS、重试、熔断和观测。
- **BFF：** 为每类客户端（网页、手机）各写一个专用后端，负责聚合多个服务的结果并裁剪成该客户端要的形状；它是有业务含义的代码，而通用网关刻意保持薄。
- **常见组合：** 网关挡在最外面，其后可跟 BFF，服务之间走网格；不要把聚合与业务逻辑塞进网关本身。
- **2026 亮点：** 东西向不必默认每个 Pod 一个 sidecar：Istio ambient 已 GA，节点级 ztunnel 负责 mTLS 和四层策略，只给需要七层策略的服务加 waypoint 代理，两种模式可在同一网格共存。代价是 waypoint 多一跳、要独立伸缩，多集群场景仍要评估。
