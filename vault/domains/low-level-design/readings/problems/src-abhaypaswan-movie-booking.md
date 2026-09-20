---
nodes: [problems.booking.movie-booking]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/movie-ticket-booking
---
# lld-python — Design a Movie Ticket Booking System

值得读：少见的纯 Python 题解（MIT 许可），开篇就把"两个人同时点同一个座位"点为全题唯一的难点，
和本题解的判断一致；它用一个独立的 `SeatLockManager` 持有全局锁表加一把 `RLock`，过期时间是
`time.monotonic()` 的浮点时间戳。两点分歧：本题解把锁座状态下放到 `Show` 内部，让真源只有一份、
锁的粒度自然落在场次上；时间一律用注入的 `datetime` 时钟，于是超时可以在不 `sleep` 的情况下测出来。
它的分层（Repository / Facade）比本题解重，可作为"面试官明确要求分层"时的参照。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/abhaypaswan/lld-python/tree/main/problems/movie-ticket-booking)

## Archived copy
![[src-abhaypaswan-movie-booking-clip]]
%% trellis:end %%
