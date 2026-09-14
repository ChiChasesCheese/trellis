---
id: architecture-schema-compat-rules
node: architecture.discovery
type: qa
---
## Q
You must evolve an event/API schema while old consumers and old producers are still live. Which changes are safe, and which direction of compatibility do you need?

## A
Safe (compatible) changes: **add optional fields with defaults**; never remove, rename, retype, or reuse a field/tag number — deprecate and leave it.

- **Backward compatibility**: new readers handle old data — needed to read history (logs, stored events).
- **Forward compatibility**: old readers tolerate new data (ignore unknown fields) — needed because producers upgrade before consumers (or vice versa) during rolling deploys.
- In a log-based world you effectively need **both** ("full" compatibility), enforced mechanically by a **schema registry** that rejects breaking publishes — not by code review.

## Q zh
你必须在旧消费者和旧生产者仍然活跃时演进一个事件/API schema。哪些改变是安全的，你需要哪个方向的兼容性？

## A zh
安全（兼容）改变：**添加有默认的可选字段**；永不移除、重命名、重新输入或重用字段/标记号——弃用并留下。

- **向后兼容**：新读者处理旧数据——需要读历史（日志、存储事件）。
- **向前兼容**：旧读者容忍新数据（忽略未知字段）——需要因为生产者在消费者升级前升级（或反之）在滚动部署期间。
- 在基于日志的世界中，你有效需要**两者**（"完整"兼容），由拒绝破坏发布的**schema 注册表**机械强制——不是代码审查。
