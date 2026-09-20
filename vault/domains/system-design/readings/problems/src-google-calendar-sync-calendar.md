---
nodes: [problems.realtime.calendar]
url: https://developers.google.com/workspace/calendar/api/guides/sync
---
# Google Calendar API — Synchronize resources efficiently

值得读：说明了 Google Calendar API 的增量同步机制——`syncToken`/`nextSyncToken`、
分页时的 `nextPageToken`、以及游标失效时返回 HTTP `410 Gone` 要求客户端清空本地状态
重新全量同步。比多数题解文章更具体的地方是：它是一个真实生产系统对"游标失效"给出的
具体、可验证的行为（`410 Gone`），本题解「深入探讨」第 6 节的同步端点直接采用这个具体
行为，同时和 RFC 6578 的前置条件失败语义做了明确区分,没有假设两者完全等价。
