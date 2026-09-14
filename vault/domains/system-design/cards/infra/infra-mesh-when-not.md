---
id: infra-mesh-when-not
node: infra.mesh
type: qa
---
## Q
When is a service mesh not worth adopting?

## A
- **Few services or a single language**: a shared library plus an API gateway covers TLS, retries, and metrics with far less machinery.
- **Mostly north-south traffic**: meshes govern service-to-service (east-west) calls; if a gateway fronts a monolith or a couple of backends, there's little east-west to manage.
- **No platform team**: a mesh is a product you operate — control plane upgrades, proxy versioning, CRD sprawl.

It earns its keep with **many polyglot services**, a compliance mandate for uniform mTLS/authz, or cross-team traffic-policy needs (splits, mirroring) — i.e. when the alternative is N teams reimplementing the same guarantees.

## Q zh
什么时候服务网格不值得采用？

## A zh
- **少数服务或单一语言**：共享库加 API 网关覆盖 TLS、重试和指标，远少机制。
- **主要北南流量**：网格管理服务-到-服务（东西）调用；如果网关前有单体或几个后端，有很少东西要管理。
- **无平台团队**：网格是你操作的产品——控制平面升级、proxy 版本、CRD 蔓延。

它用**许多 polyglot 服务**、统一 mTLS/authz 的合规mandate 或跨团队流量策略需要（分割、镜像）赚取——即当替代是 N 个团队重新实现相同保证。
