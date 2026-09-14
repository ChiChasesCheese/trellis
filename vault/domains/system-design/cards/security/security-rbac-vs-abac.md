---
id: security-rbac-vs-abac
node: security.authz
type: qa
---
## Q
When does RBAC stop being enough and force a move toward ABAC (or relationship-based) authorization?

## A
RBAC (user → roles → permissions) breaks when the decision depends on **context the role can't encode**:

- **Resource ownership/relationships**: "editors can edit *documents in their own workspace*" — pure RBAC needs a role per workspace (role explosion); ReBAC systems (Zanzibar-style, e.g. SpiceDB/OpenFGA) model this directly.
- **Runtime attributes**: time of day, device posture, data classification, tenant of the request.

Rule of thumb: RBAC for coarse, stable job functions; ABAC/ReBAC when policies mention properties of the **resource or environment**, not just the user.

## Q zh
RBAC 何时停止足够并强制向 ABAC（或基于关系）授权移动？

## A zh
RBAC（用户 → 角色 → 权限）当决定依赖于**角色无法编码的上下文**时破裂：

- **资源所有权/关系**：「编辑可编辑*其自己工作区的文档*」— 纯 RBAC 需每工作区一个角色（角色爆炸）；ReBAC 系统（Zanzibar 风格，如 SpiceDB/OpenFGA）直接建模。
- **运行时属性**：一天时间、设备姿态、数据分类、请求的租户。

经验法则：RBAC 用于粗粒度、稳定工作职能；ABAC/ReBAC 当策略提及**资源或环境**的属性，不仅用户。
