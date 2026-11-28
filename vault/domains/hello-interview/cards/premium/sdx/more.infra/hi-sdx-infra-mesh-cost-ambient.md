---
id: hi-sdx-infra-mesh-cost-ambient
node: more.infra
type: qa
step: 11
---
## Q
**网格的代价与 ambient 模式**｜补充 · 平台基础设施：容器、服务网格、发布 · 加分

面试官：「sidecar 网格在延迟和运维上有什么代价？ambient（无 sidecar）模式又怎样重新分配这笔代价？」

## A
**结论。** sidecar 的代价是每跳多两次代理（调用方的 sidecar 出、被调方的 sidecar 入），每个 Pod 都要一份代理的资源，代理升级和 Pod 重启绑在一起。ambient 把代理拆开：每个节点一个共享的四层隧道负责 mTLS 和遥测，七层的 waypoint 代理只给需要 HTTP 级策略的服务部署。

**要点。**
- **延迟：** 每一跳多两次代理转发，调用链越深，叠加越明显。
- **资源：** Istio 官方基准（1.24，每秒 1000 请求）里，一个 sidecar 约占 0.20 vCPU 和 60 MB 内存，且每个 Pod 一份；而节点级的 ztunnel 约占 0.06 vCPU 和 12 MB。
- **运维：** 代理版本和 Pod 生命周期耦合，排障时多一层。
- **ambient：** 只有用到七层策略的路由才付七层的代价。
- **2026 亮点：** Istio ambient 自 1.24 起已 GA，可以放心讲：节点上的 ztunnel 只做 mTLS、四层授权和遥测，需要重试、按路径路由、七层鉴权的服务才加 waypoint（Envoy，独立部署、独立伸缩），并且和 sidecar 能在同一个网格里共存、按服务逐步迁移。代价是 waypoint 多一跳、要单独做容量规划，ambient 的多集群/多网络能力仍是 Beta，跨集群大规模场景要先评估。

**面试里这样说。** 「sidecar 的代价是每个 Pod 一份代理和每跳两次转发。如果只要 mTLS 和遥测，我会选 ambient 的节点级隧道，只对需要七层策略的服务单独加 waypoint。」

**易错。**
- **只算延迟、不算资源：** 几百个 Pod 每个一个代理，内存和 CPU 的账很可观。
- **以为 ambient 完全没有代理：** 它只是把代理挪到节点和 waypoint 上。
