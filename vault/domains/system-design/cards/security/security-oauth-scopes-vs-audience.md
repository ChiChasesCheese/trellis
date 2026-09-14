---
id: security-oauth-scopes-vs-audience
node: security.authn.oauth
type: qa
---
## Q
Scopes vs audience: what does each one constrain, and why is "the token has scope `orders:read`, so let the request through" an authorization bug?

## A
- **Scope** = *what the user delegated to this client* — a coarse, consent-visible capability (`orders:read`). It only ever **narrows** what the client may ask for.
- **Audience (`aud`)** = *which resource server may accept this token*. Every RS must reject tokens not minted for it (along with `iss`, signature, `exp`), or a token issued for the low-value analytics service can be replayed against the payments service — a classic confused deputy.

The bug is treating scope as a permission check. Scope says the client is *allowed to ask*; it says nothing about whether **this subject** owns **this object**. You still need the object-level check: `order.tenant_id == token.tenant_id`, `order.user_id == token.sub`. Effective permission is the **intersection** of the user's real rights and the token's scope.

Practical rule: request per-resource tokens (`resource`/`audience` parameter at the token endpoint) so a leak is bounded to one service, and keep scopes coarse — fine-grained policy belongs in the resource server, not in the token.

## Q zh
Scope vs audience：各限制什么，为什么「token 有 scope `orders:read`，所以让请求通过」是授权 bug？

## A zh
- **Scope** = *用户委托给这个客户端什么* — 粗粒度、同意可见能力（`orders:read`）。它仅**缩小**客户端可能要求的。
- **Audience（`aud`）** = *哪个资源服务器可接受这个 token*。每个 RS 必须拒绝非为它铸造的 token（连同 `iss`、签名、`exp`），否则为低价值分析服务发行的 token 可针对支付服务重放 — 经典混淆代理。

bug 是把 scope 当做权限检查。Scope 说客户端*允许要求*；它对**这个主体**是否拥有**这个对象**什么都不说。你仍需对象级检查：`order.tenant_id == token.tenant_id`、`order.user_id == token.sub`。有效权限是用户真实权限和 token 范围的**交集**。

实际规则：在 token 端点请求按资源 token（`resource`/`audience` 参数）所以泄漏绑定到一个服务，保持 scope 粗粒度 — 细粒度策略属于资源服务器，不是 token。
