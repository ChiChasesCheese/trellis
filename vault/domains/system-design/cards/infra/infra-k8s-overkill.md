---
id: infra-k8s-overkill
node: infra.containers
type: qa
---
## Q
When is Kubernetes over-engineering, and what do you run instead?

## A
K8s charges a **platform tax** — cluster upgrades, networking/ingress/observability stack, YAML sprawl, and in practice a platform team to own it. That tax is overkill when you have a handful of ordinary HTTP services, a small team, and no special scheduling needs.

- Instead: **managed container platforms** (Cloud Run, Fargate/ECS) give per-container deploys and autoscaling with no cluster to operate; a monolith on a PaaS stays viable longer than most teams admit.
- Adopt k8s when you're otherwise *building* its features — custom scheduling, service discovery, batch/GPU orchestration — or need its ecosystem (operators) across many teams.

## Q zh
什么时候 Kubernetes 是过度设计，你改为运行什么？

## A zh
K8s 收取**平台税**——集群升级、网络/ingress/observability 栈、YAML 蔓延，实际上是一个平台团队来拥有它。当你有一把普通 HTTP 服务、小团队、无特殊调度需要时那个税是过度的。

- 反之：**托管容器平台**（Cloud Run、Fargate/ECS）给每容器部署和自动扩展无需操作集群；单体在 PaaS 上比大多数团队承认的保持更长的活力。
- 当你另外**构建**它的特性时采用 k8s——自定义调度、服务发现、batch/GPU 编排——或跨许多团队需要它的生态（operator）。
