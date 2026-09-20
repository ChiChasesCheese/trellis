---
id: problems-auth-service-refresh-rotation-reuse-detection
node: problems.foundations.auth-service
type: qa
step: 4
tags: [grown]
---
## Q
In an authentication service, how does refresh-token rotation turn a stolen refresh token into a detectable event, and what should the server do when it detects reuse?

## A
Every call to the refresh endpoint issues a brand-new refresh token and invalidates the one just used, so each token is single-use. If a stolen token is used by an attacker before the legitimate client refreshes, the legitimate client's next refresh attempt will present an already-invalidated token — and vice versa if the legitimate client refreshes first. Either way, presenting an already-rotated token is proof that two parties hold tokens from the same lineage. The server's response is to revoke the entire token family (the whole session lineage), forcing both the attacker and the legitimate user to re-authenticate, rather than trying to distinguish which party is legitimate.

## Q zh
在认证服务中，refresh token 轮换如何把被盗的 refresh token 变成可检测事件，检测到重用时服务器应该做什么？

## A zh
每次调用 refresh 端点都会发放一个全新的 refresh token 并使刚用过的那个失效，所以每个 token 只能用一次。如果被盗的 token 在合法客户端刷新之前被攻击者使用，合法客户端下一次刷新时呈现的就是一个已失效的 token——反之，如果合法客户端先刷新也是同样的结果。无论哪种情况，呈现一个已轮换过的 token 就是两方持有同一血统 token 的证据。服务器的响应是撤销整个 token family（整条会话血统），强制攻击者和合法用户都重新认证，而不是试图分辨哪一方才是合法的。
