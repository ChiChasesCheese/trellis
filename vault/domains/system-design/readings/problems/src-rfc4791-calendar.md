---
nodes: [problems.realtime.calendar]
url: https://www.rfc-editor.org/rfc/rfc4791
---
# RFC 4791 — Calendaring Extensions to WebDAV (CalDAV)

值得读：定义了日历作为 WebDAV 资源集合的访问协议，尤其是把 `calendar-query`（返回完整
事件数据）和 `free-busy-query`（只返回忙闲区间）明确区分成两种不同权限的 REPORT 方法。
比多数题解文章更具体的地方是：这个区分直接对应本题解「深入探讨」第 4 节"free/busy 查询
不应该暴露事件详情"这条设计,不是本设计自己发明的权限边界,而是协议层面就已经这样划分。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.rfc-editor.org/rfc/rfc4791)

## Archived copy
![[src-rfc4791-calendar-clip]]
%% trellis:end %%
