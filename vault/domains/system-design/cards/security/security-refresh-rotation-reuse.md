---
id: security-refresh-rotation-reuse
node: security.authn.tokens
type: qa
---
## Q
How does refresh token rotation turn token theft into a detectable event, and what happens on reuse?

## A
**Rotation**: every refresh issues a *new* refresh token and invalidates the one just used — each token is single-use, so a stolen refresh token stops working as soon as either party (thief or legitimate client) refreshes next.

**Reuse detection**: if an already-rotated token is presented again, two parties hold tokens from the same lineage — proof of theft. The server revokes the **entire token family** (the whole session), forcing re-authentication for both.

This is why rotation is mandatory for refresh tokens in browsers/SPAs, where long-lived tokens can't be stored safely. Builds on [[security-access-refresh-tokens]].

## Q zh
refresh token 轮换如何把 token 盗窃变成可检测事件，重用时发生什么？

## A zh
**轮换**：每次刷新发*新* refresh token 并使刚用的一个失效 — 各 token 单次使用，所以偷的 refresh token 一旦任何一方（小偷或合法客户端）下次刷新就停止工作。

**重用检测**：如果已轮换的 token 再次呈现，两方持有来自同一血统的 token — 盗窃证明。服务器撤销**整个 token 族**（整个会话），强制双方重新认证。

这是为什么轮换对浏览器/SPA 中的 refresh token 强制，那里长生命周期 token 无法安全存储。建立于 [[security-access-refresh-tokens]]。
