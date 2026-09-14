---
id: architecture-boundaries-data-ownership
node: architecture.services
type: qa
---
## Q
What's the rule for drawing service boundaries, and why is a shared database between services considered the cardinal sin?

## A
Rule: a service **exclusively owns its data** — boundary drawn around a business capability (bounded context), and all access to that data goes through the service's API or its published events.

A shared database silently couples the services back together:
- Any **schema change breaks unknown readers** — you've recreated the monolith's coupling but without the compiler, tests, or atomic deploy that made it manageable.
- Ownership of invariants is ambiguous: two writers, no one accountable for consistency.

Consequence to say out loud: no cross-service joins or transactions — you get API composition, data replication via events, and eventual consistency instead. If two "services" constantly need each other's tables, they're one service.

## Q zh
绘制服务边界的规则是什么，为什么服务之间共享数据库被认为是基本罪恶？

## A zh
规则：一个服务**专属拥有其数据** ——边界围绕业务能力（有界上下文），对该数据的所有访问通过服务的 API 或其发布事件。

共享数据库默默耦合服务回一起：
- 任何**schema 改变打破未知读者** ——你重新创建了整体的耦合但没有编译器、测试或使其可管理的原子部署。
- 不变量的所有权模糊：两个写者，没有人对一致性负责。

说出来的后果：没有跨服务连接或事务——你获得 API 组合、通过事件的数据复制和最终一致性代替。如果两个"服务"不断需要彼此的表，它们是一个服务。
