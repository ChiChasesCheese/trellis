---
nodes: [problems.realtime.calendar]
url: https://developers.google.com/workspace/calendar/api/v3/reference/events
---
# Google Calendar API — Events resource reference

值得读：说明了循环事件的单个实例被单独修改后如何表示——`recurringEventId` 指回主系列、
`originalStartTime` 记录"如果没被修改本该发生的时刻"、同一系列的所有发生共享同一个
`iCalUID` 但各自拥有独立的 `id`。比多数题解文章更具体的地方是：它是一个真实生产 API
对 RFC 5545 的 RECURRENCE-ID 概念的具体字段级实现,本题解「核心实体与 API」的
`EventException` 设计参照了这个具体字段划分。

%% trellis:begin %%
## Source
[Open the original ↗](https://developers.google.com/workspace/calendar/api/v3/reference/events)

## Archived copy
![[src-google-calendar-events-calendar-clip]]
%% trellis:end %%
