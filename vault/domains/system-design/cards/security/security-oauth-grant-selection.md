---
id: security-oauth-grant-selection
node: security.authn.oauth
type: qa
---
## Q
Pick the grant: (a) a nightly batch job calling a partner API, (b) a web app acting for a signed-in user, (c) a smart TV app. What makes (a) fundamentally different from the others?

## A
- (a) **Client credentials** — the app authenticates *as itself* with a secret or (better) mTLS / signed JWT assertion.
- (b) **Authorization code + PKCE** — a user is present and consents to delegation.
- (c) **Device authorization grant** — the TV shows a code, the user completes the flow on a phone, and the device polls the token endpoint.

The difference: client credentials has **no resource owner**. The token carries no `sub` for a human and no consent, so the resource server must authorize on the **client's** identity and scopes, and any per-user data access has to be constrained some other way (tenant-scoped credentials, an explicit `act`/on-behalf-of exchange). Treating a client-credentials token as "some user" is how batch jobs end up with cross-tenant reach.

Two anti-patterns: using client credentials from a browser or mobile app (a **public client** cannot hold a secret — use code+PKCE), and password grant (ROPC), which is removed in OAuth 2.1 because it hands your credentials to the client and cannot do MFA or federation.

## Q zh
选择授权：(a) 夜间批处理调用合作伙伴 API，(b) web 应用作用于已登录用户，(c) 智能电视应用。什么让 (a) 从根本上不同于其他？

## A zh
- (a) **客户端凭证** — 应用以*自己*认证用秘密或（更好）mTLS / 签名 JWT 断言。
- (b) **授权代码 + PKCE** — 用户存在且同意委托。
- (c) **设备授权授予** — 电视显示代码，用户在电话上完成流程，设备轮询 token 端点。

差异：客户端凭证无**资源所有者**。token 无人的 `sub` 也无同意，所以资源服务器必须在**客户端**身份和 scope 上授权，任何按用户数据访问必须以其他方式约束（租户范围凭证、显式 `act`/代表交换）。将客户端凭证 token 当做「某个用户」是批处理如何以跨租户达成。

两个反模式：从浏览器或移动应用使用客户端凭证（**公共客户端**无法持有秘密 — 用 code+PKCE），和密码授予（ROPC），在 OAuth 2.1 中移除因为它把你的凭证传给客户端，无法做 MFA 或联盟。
