---
nodes: [problems.realtime.calendar]
url: https://www.rfc-editor.org/rfc/rfc5545
---
# RFC 5545 — Internet Calendaring and Scheduling Core Object Specification (iCalendar)

值得读：定义了 RRULE 循环规则的完整语法（FREQ/INTERVAL/COUNT/UNTIL/BYDAY 等）、用
EXDATE 和 RECURRENCE-ID 表达循环事件例外的机制、以及用 TZID 参数配合 VTIMEZONE 组件
存储"本地时间+时区"而不是固定 UTC 偏移量的方式。比多数题解文章更具体的地方是：它是
"存规则不存实例"和"本地时间+时区标识符"这两个设计决策的原始规范来源，不是某个公司的
私有约定，本题解的核心数据模型直接对齐这份规范。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.rfc-editor.org/rfc/rfc5545)

## Archived copy
![[src-rfc5545-calendar-clip]]
%% trellis:end %%
