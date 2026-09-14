---
id: security-confused-deputy
node: security.authz
type: qa
---
## Q
An internal reporting service with read access to *all* tenants' data serves any caller that asks. A low-privilege client requests another tenant's report and gets it. Name the vulnerability class and the fix.

## A
**Confused deputy**: a privileged service is tricked into using *its own* authority on behalf of a less-privileged caller. Classic instances: internal services trusting any in-network caller, SSRF against cloud metadata endpoints (the VM is the deputy), cross-account access without an external ID.

Fix — make authorization decisions on the **originating principal**, not the deputy:

- **Propagate end-user/tenant context** through the call chain (on-behalf-of token exchange, signed user context), and check it at the data layer.
- Scope the deputy's own credentials down (per-tenant creds, external IDs for cross-account roles) so it *cannot* over-reach even when confused.

## Q zh
内部报告服务对*所有*租户数据有读权限，为任何来问的调用者服务。低权限客户端请求另一租户的报告并得到。命名漏洞类别和修复。

## A zh
**混淆代理**：特权服务被骗以*自己的*权限代表低权限调用者行动。经典例子：内部服务信任任何网内调用者、SSRF 对云元数据端点（VM 是代理）、跨账户访问无外部 ID。

修复 — 在**源主体**上做授权决定，不是代理：

- **传播最终用户/租户上下文**通过调用链（代表交换 token、签名用户上下文），在数据层检查。
- 缩小代理自己凭证范围（每租户凭证、跨账户角色的外部 ID），所以它*不能*过度，即使混淆。
