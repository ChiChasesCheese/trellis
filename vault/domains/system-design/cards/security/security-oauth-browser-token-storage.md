---
id: security-oauth-browser-token-storage
node: security.authn.oauth
type: qa
---
## Q
Why was the implicit flow deprecated, and — since code+PKCE replaced it — where should an SPA keep the resulting tokens in 2026?

## A
**Implicit died** because it returned the access token in the **URL fragment**: it leaked into browser history, referrers, logs and extensions; it was unbound (no PKCE, no client authentication, so a token could be injected from another flow); and it could not issue refresh tokens, forcing either long-lived access tokens or hidden-iframe renewals that third-party cookie blocking has since killed.

PKCE fixes *code interception*, not *token custody* — the SPA still ends up holding a bearer token in JS, where any XSS or compromised npm dependency exfiltrates it.

The 2026 default is the **BFF (backend-for-frontend)**: a server-side component runs the code+PKCE exchange, keeps access/refresh tokens server-side, and gives the browser only an `HttpOnly; Secure; SameSite` session cookie, proxying API calls. If tokens must live in the browser, the minimum bar is: in-memory only (never `localStorage`), short access-token TTL, **rotating refresh tokens with reuse detection**, and ideally sender-constrained (DPoP) tokens so a stolen one is not replayable.

## Q zh
为什么隐式流被弃用，既然 code+PKCE 替代了它 — 2026 年 SPA 应该把生成的 token 放哪里？

## A zh
**隐式死了**因为它在 **URL 片段**返回 access token：它泄漏进浏览器历史、引用方、日志和扩展；它无约束（无 PKCE、无客户端认证，token 可被从另一流程注入）；它不能发 refresh token，强制长生命周期 access token 或隐藏 iframe 续期，现在被第三方 cookie 阻止杀死。

PKCE 修复*代码拦截*，不是*token 保管* — SPA 仍然以 JS 中的 bearer token 结束，任何 XSS 或破坏的 npm 依赖外流它。

2026 默认是 **BFF（backend-for-frontend）**：服务端组件运行 code+PKCE 交换，保存 access/refresh token 在服务端，仅给浏览器 `HttpOnly; Secure; SameSite` 会话 cookie，代理 API 调用。如果 token 必须活在浏览器，最小栏是：仅内存（绝不 `localStorage`）、短 access-token TTL、**带重用检测的轮换 refresh token**，理想上发送方约束（DPoP）token 所以偷的一个无法重放。
