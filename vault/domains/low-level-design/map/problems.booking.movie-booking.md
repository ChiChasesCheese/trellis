%% trellis:begin %%
# 电影订票（BookMyShow）
*设计题（Design Problems） / 预订与库存*

影院-影厅-场次-座位的层级模型，选座锁定、超时释放与并发下单。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/structure.storage|内存持久化（In-Memory Persistence）]], [[domains/low-level-design/map/concurrency.primitives|同步原语（threading）]]

## Readings
- [[solution-movie-booking|设计题解：电影订票（BookMyShow）]]
- [[src-abhaypaswan-movie-booking|lld-python — Design a Movie Ticket Booking System]]
- [[src-ashishps1-movie-booking|awesome-low-level-design — Movie Ticket Booking System]]
- [[src-codezym-movie-booking|CodeZymSolutions — q10 Movie Booking App]]

## Drills
- [[design-movie-booking|Drill：电影订票（BookMyShow）]]

## Cards (8)
1. [[problems-movie-booking-seat-two-layers]]
2. [[problems-movie-booking-who-owns-hold-state]]
3. [[problems-movie-booking-all-or-nothing-hold]]
4. [[problems-movie-booking-lazy-expiry]]
5. [[problems-movie-booking-lock-granularity]]
6. [[problems-movie-booking-payment-outside-lock]]
7. [[problems-movie-booking-no-pending-status]]
8. [[problems-movie-booking-policies-dont-touch-locks]]
%% trellis:end %%

## Notes
