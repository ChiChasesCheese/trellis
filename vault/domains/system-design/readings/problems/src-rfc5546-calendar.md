---
nodes: [problems.realtime.calendar]
url: https://www.rfc-editor.org/rfc/rfc5546
---
# RFC 5546 — iCalendar Transport-Independent Interoperability Protocol (iTIP)

值得读：定义了组织者与参会人之间调度事务的标准方法（REQUEST/REPLY/CANCEL/COUNTER 等）
和 PARTSTAT/RSVP 参数的语义。比多数题解文章更具体的地方是：它明确规定了组织者持有
master 事件、参会人只能通过 REPLY 表达自己的状态这一权限模型，本题解「核心实体与 API」
和「深入探讨」第 5 节直接沿用了这一权限边界，而不是自己假设一个对称的编辑模型。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.rfc-editor.org/rfc/rfc5546)

## Archived copy
![[src-rfc5546-calendar-clip]]
%% trellis:end %%
