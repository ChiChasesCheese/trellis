---
id: ai-spend-control-budget
node: cost.ai-token-metering
type: qa
tags: [grown]
---
## Q
想防止某个团队随手在大表上跑 LLM 函数导致 AI 费用失控，资源监控器（resource monitor）能起作用吗？应该用哪些手段？

## A
资源监控器只作用于虚拟仓库，无法跟踪或拦截 AI 服务的令牌消耗。可用的控制手段：用预算（budget）监控 AI 服务的信用点消耗并在接近上限时告警；用 RBAC 控制谁能调用 Cortex 函数（例如收回默认授予给 PUBLIC 的 Cortex 数据库角色，只授予特定角色）；通过账户级设置限制允许使用的模型，避免默认调用昂贵的大模型。
