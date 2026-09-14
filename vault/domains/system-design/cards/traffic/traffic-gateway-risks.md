---
id: traffic-gateway-risks
node: traffic.gateways
type: qa
---
## Q
What risks does putting an API gateway in front of everything create, and how is each mitigated?

## A
- **Single point of failure**: gateway down = whole product down → run it as a **stateless horizontally-scaled fleet** behind an L4 LB; config from a replicated store.
- **Latency tax**: one extra hop plus any auth/transform work on *every* request → keep per-request logic lean; ~ms budget.
- **Team bottleneck / god-box**: all routing and policy changes funnel through one component → self-serve declarative config (per-team route ownership, GitOps) instead of a central gatekeeper team.

## Q zh
在所有东西前放置 API 网关会创建什么风险，每个如何缓解？

## A zh
- **单点故障**：网关宕机 = 整个产品宕机 → 在 L4 LB 后运行它作为**无状态水平扩展舰队**；从复制存储配置。
- **延迟税**：一个额外跳跃加上任何身份验证/转换工作在*每个*请求 → 保持每个请求逻辑精简；约 ms 预算。
- **团队瓶颈 / god-box**：所有路由和策略变更通过一个组件 → 自助声明性配置（每个团队路由所有权、GitOps）而不是中央网关守护团队。
