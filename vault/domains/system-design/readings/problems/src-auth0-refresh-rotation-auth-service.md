---
nodes: [problems.foundations.auth-service]
url: https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation
tags: [engineering-blog, no-archive]
---
# Refresh Token Rotation

值得读：Auth0 官方文档，描述了刷新令牌轮换与重用检测的具体行为——每次刷新都发放
新 refresh token 并使旧的失效，重用一个已轮换过的 token 会立即撤销整条 token
family，不存在宽限期。本题解「深入探讨」第 3 节采用同样的机制，并补充了这篇文档
未涉及的部分：为什么这个存储必须和账号核心凭证记录物理分离（见深入探讨第 7 节给
出的四个数量级 QPS 差异），这是一个纯架构容量问题，不是 Auth0 文档讨论的范畴。
