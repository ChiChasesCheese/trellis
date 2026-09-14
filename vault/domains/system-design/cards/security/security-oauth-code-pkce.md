---
id: security-oauth-code-pkce
node: security.authn.oauth
type: qa
---
## Q
In the OAuth2 authorization code flow, why does the client exchange a code instead of receiving tokens directly in the redirect — and what does PKCE add?

## A
The redirect travels through the **browser** (URL, history, referrers, extensions) — an untrusted channel. The short-lived, one-time **code** is useless there because tokens are only issued on a direct **back-channel** call from the client to the token endpoint.

**PKCE** binds the code to whoever started the flow: the client sends a hash of a random verifier up front and must present the verifier at exchange, so an intercepted code can't be redeemed. Mandatory for public clients (SPAs, mobile) with no client secret — and now recommended for all clients (OAuth 2.1 default).

## Q zh
在 OAuth2 授权代码流中，为什么客户端交换代码而不在重定向中直接接收 token — PKCE 加什么？

## A zh
重定向通过**浏览器**（URL、历史、引用方、扩展）— 不信任通道。短生命周期、一次性**代码**那里没用因为 token 仅在客户端到 token 端点的直接**回通道**调用时发行。

**PKCE** 将代码绑定到启动流的人：客户端预先发随机验证器的哈希，交换时必须呈现验证器，所以拦截的代码无法赎回。对无客户端秘密的公共客户端（SPA、移动）强制 — 现在对所有客户端推荐（OAuth 2.1 默认）。
