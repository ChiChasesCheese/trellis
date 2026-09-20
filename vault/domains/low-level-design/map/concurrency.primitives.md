%% trellis:begin %%
# 同步原语（threading）
*并发（Concurrency）*

`Lock`、`RLock`、`Condition`、`Semaphore`、`Event`、`queue.Queue`：各自解决的问题与误用方式。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/concurrency.model|线程、GIL 与内存模型]]

**Unlocks:** [[domains/low-level-design/map/concurrency.hazards|死锁及其亲戚]], [[domains/low-level-design/map/concurrency.patterns|并发模式]], [[domains/low-level-design/map/problems.machines.coffee-machine|咖啡机（Coffee Machine）]], [[domains/low-level-design/map/problems.booking.movie-booking|电影订票（BookMyShow）]], [[domains/low-level-design/map/problems.marketplaces.online-auction|在线拍卖（Online Auction）]], [[domains/low-level-design/map/problems.components.rate-limiter|限流器（Rate Limiter）]], [[domains/low-level-design/map/problems.components.bounded-blocking-queue|有界阻塞队列（Bounded Blocking Queue）]]

## Readings
- [[java-concurrency-in-practice|Java Concurrency in Practice (Goetz et al.)]]
- [[jenkov-read-write-locks|Read / Write Locks in Java (Jakob Jenkov)]]
- [[preshing-lock-free|An Introduction to Lock-Free Programming (Jeff Preshing)]]

## Drills
- [[design-atm|Drill：ATM 取款机（ATM）]]
- [[design-bounded-blocking-queue|Drill：有界阻塞队列（Bounded Blocking Queue）]]
- [[design-coffee-machine|Drill：咖啡机（Coffee Machine）]]
- [[design-movie-booking|Drill：电影订票（BookMyShow）]]
- [[design-online-auction|Drill：在线拍卖（Online Auction）]]
- [[design-rate-limiter|Drill：限流器（Rate Limiter）]]
- [[design-stock-brokerage|Drill：股票交易系统（Stock Brokerage）]]
- [[design-ttl-cache|Drill：带过期时间的缓存（TTL Cache）]]

## Cards (5)
1. [[concurrency-lock-rlock]]
2. [[concurrency-mutex-vs-semaphore]]
3. [[concurrency-condvar-wait-loop]]
4. [[concurrency-event]]
5. [[concurrency-queue-vs-deque]]
%% trellis:end %%

## Notes
