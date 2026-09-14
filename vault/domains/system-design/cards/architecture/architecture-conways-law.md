---
id: architecture-conways-law
node: architecture.services
type: qa
---
## Q
Conway's law says architecture copies org structure. How do mature orgs use it as a *design input* rather than a curse?

## A
**Inverse Conway maneuver**: since the system will mirror team communication paths anyway, design the *teams* to match the architecture you want — one long-lived team per service group, each owning its services end-to-end (build, run, on-call).

Practical consequences:

- A service boundary that **splits across two teams** will erode into chatty coupling and unclear ownership — redraw the boundary or merge the teams.
- **Team cognitive load caps service scope**: split when a team can no longer hold its domain, not at some ideal "microservice size."
- Interview signal: justify boundaries by *ownership and change patterns* ([[architecture-boundaries-data-ownership]]), not by technology layers.

## Q zh
Conway 定律说架构复制组织结构。成熟组织如何将其用作*设计输入*而不是诅咒？

## A zh
**反向 Conway 机动**：由于系统无论如何都会镜像团队沟通路径，设计*团队*来匹配你想要的架构——一个长期团队每个服务组，每个端到端拥有其服务（构建、运行、待命）。

实际后果：

- 一个服务边界**跨两个团队分裂**将侵蚀成啰嗦耦合和不清楚所有权——重新绘制边界或合并团队。
- **团队认知负荷限制服务范围**：当团队不再能拥有其域时分裂，不是在某个理想的"微服务大小"。
- 面试信号：通过*所有权和改变模式*证明边界（[[architecture-boundaries-data-ownership]]），不是通过技术层。
