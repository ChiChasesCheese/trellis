---
id: security-oauth-vs-oidc
node: security.authn.oauth
type: qa
---
## Q
"Log in with Google" — is that OAuth2 or OIDC, and why is using a plain OAuth2 access token as proof of identity a bug?

## A
That's **OIDC** — an identity layer on top of OAuth2. OAuth2 alone answers "may this app access this resource?" (**delegation**); it says nothing about who the user is.

An access token is not audience-bound to your app: any app the user granted a token to could replay it against your backend and impersonate them. OIDC fixes this with the **ID token** — a JWT with the user's identity, signed by the provider, with an `aud` claim naming your client and a nonce — made to be verified, not forwarded.

## Q zh
「用 Google 登录」— 那是 OAuth2 还是 OIDC，为什么用纯 OAuth2 access token 作为身份证明是 bug？

## A zh
那是 **OIDC** — OAuth2 之上的身份层。OAuth2 单独回答「这个应用可访问这个资源吗？」（**委托**）；它对用户是谁什么都不说。

access token 不是你应用的 audience 约束：用户授予 token 的任何应用可对你后端重放它并冒充他们。OIDC 用 **ID token** 修复 — 带用户身份的 JWT，由提供者签名，有命名你客户端的 `aud` 声明和 nonce — 制造来验证，不转发。
