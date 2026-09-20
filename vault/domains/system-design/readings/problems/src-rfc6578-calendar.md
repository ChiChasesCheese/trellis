---
nodes: [problems.realtime.calendar]
url: https://www.rfc-editor.org/rfc/rfc6578
---
# RFC 6578 — Collection Synchronization for WebDAV (sync-collection)

值得读：定义了 `sync-token` 增量同步机制,以及服务端在无法继续维护完整变更历史时,通过
`DAV:valid-sync-token` 前置条件失败要求客户端退回全量同步的语义。比多数题解文章更具体
的地方是：它把"游标失效"当作协议里明确定义的一等情形,而不是一个需要临时补救的边缘
情况——本题解「深入探讨」第 6 节引用它作为增量同步设计的参照,同时特意说明本设计的同步
端点在游标失效时选择了和 Google Calendar API 的 `410 Gone` 更接近的具体行为,没有把
两种协议的失效语义混为一谈。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.rfc-editor.org/rfc/rfc6578)

## Archived copy
![[src-rfc6578-calendar-clip]]
%% trellis:end %%
