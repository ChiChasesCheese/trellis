---
nodes: [problems.foundations.auth-service]
url: https://www.rfc-editor.org/rfc/rfc9700.html
tags: [reference]
---
# RFC 9700 — Best Current Practice for OAuth 2.0 Security

值得读：OAuth 工作组官方安全最佳实践 RFC，要求公共客户端（浏览器/移动端）的
refresh token 必须是发送方约束的（sender-constrained）或使用轮换机制，并把 PKCE
的 `S256` 方法列为强制、redirect URI 校验要求精确字符串匹配。本题解「深入探讨」
第 3 节采用的正是这份 RFC 要求的轮换机制，并补充了轮换本身如何和 refresh token 的
独立容量设计（深入探讨第 7 节）结合——这部分是 RFC 本身不涉及的架构层面问题。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.rfc-editor.org/rfc/rfc9700.html)

## Archived copy
![[src-rfc9700-auth-service-clip]]
%% trellis:end %%
