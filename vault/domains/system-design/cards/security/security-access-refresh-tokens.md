---
id: security-access-refresh-tokens
node: security.authn.tokens
type: qa
---
## Q
Why pair a short-lived access token (~5–15 min) with a long-lived refresh token, instead of one long-lived token?

## A
It splits the two jobs a single token can't do at once:

- The **access token** is verified statelessly on every request; keeping it short bounds the damage window if stolen and makes revocation "wait out the TTL."
- The **refresh token** is presented rarely, only to the auth server — the one place that checks server-side state, so it **can** be revoked instantly.

Modern hardening: **refresh token rotation** — each use issues a new one; reuse of an old refresh token signals theft and kills the whole session family.

## Q zh
为什么配对一个短生命周期 access token（~5-15 分钟）和长生命周期 refresh token，而不是一个长生命周期 token？

## A zh
分离单个 token 无法同时做的两个工作：

- **access token** 在每个请求上无状态验证；保持短生命周期限制盗窃时的损害窗口，并让撤销「等待 TTL 过期」。
- **refresh token** 极少呈现，仅到 auth 服务器 — 唯一检查服务器端状态的地方，所以它**能**立即被撤销。

现代加固：**refresh token 轮换** — 每次使用发新的；老 refresh token 的重用表示盗窃并杀掉整个会话族。
