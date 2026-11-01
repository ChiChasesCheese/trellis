---
id: hi-x-lld-concurrency-locking-3-choose
node: lld.cross.lld-concurrency-locking
type: qa
step: 3
---
## Q
**类设计中的并发：锁粒度与线程模型 (Locking / Thread-safety)**｜跨题模式 · 怎么选

面对一道类设计题里的并发追问，怎么选锁粒度或线程模型？请按判断信号分支，各举一题。

## A
1. **状态是不是只有一个小结构、竞争低？** 是：一把锁就够，先写对再谈优化。例：[[kv-store-eviction|可配置淘汰策略的内存键值存储]]（面试里说明分段是下一步）。
2. **key 很多、各自独立？** 是：分段锁（16 到 64 段），不同 key 大概率落在不同段，锁数量固定，内存小。例：[[tt-per-merchant-rate-limit|按商户限流]]、[[recently-viewed-items|"最近浏览"记录]]。
3. **有两层结构（外层 map 加内层状态）？** 是：定好层次，外层锁只保护结构变化，先释放再取内层锁。例：[[rate-limiter-system|限流器（单机类设计）]]。
4. **读操作也会修改结构？**（LRU 的 `get`）是：读也要拿写锁。例：[[kv-store-eviction|可配置淘汰策略的内存键值存储]]。
5. **临界区里需要调用慢的外部服务？** 是：不持锁调用，回报结果时重新加锁并核对状态代号。例：[[api-circuit-breaker|熔断器]]；付款放在数据库事务之外的例子见 [[event-ticket-booking|活动票务预订后端]]。
6. **状态在数据库里、多个进程竞争？** 是：悲观锁、乐观版本号、带条件的原子更新，热点上首选条件更新。例：[[event-ticket-booking|活动票务预订后端]]。
7. **状态变化是一串有序的事件，或要写同一个文件？** 是：线程封闭，一个线程持有状态，其他线程通过队列投递。例：[[elevator-design|电梯系统]]、[[multithreaded-logging-framework|多线程日志框架]]。
