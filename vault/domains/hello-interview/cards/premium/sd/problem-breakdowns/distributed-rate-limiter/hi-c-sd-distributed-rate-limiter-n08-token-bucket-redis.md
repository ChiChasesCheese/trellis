---
id: hi-c-sd-distributed-rate-limiter-n08-token-bucket-redis
node: sd.problem-breakdowns.distributed-rate-limiter.notes
type: qa
step: 8
---
## Q
**分布式限流器 · 令牌桶放进 Redis：流程与竞态**｜摘要 · 必会

多个网关怎么共享令牌桶状态？为什么即使用了 MULTI/EXEC 还有竞态，怎么根治？

## A
- **为什么要集中：** 如果桶放在每个网关的本地内存，就回到进程内的问题：Alice 的 50 次请求打到网关 A、50 次打到网关 B，各自都以为没超。所以用 Redis 做所有网关的唯一事实来源。
- **流程：**
  1. 请求到达网关，用 `HMGET alice:bucket tokens last_refill` 读状态；
  2. 按流逝时间算应补多少令牌，不超过容量；
  3. 在 MULTI/EXEC 里写回令牌数和时间戳，并设 `EXPIRE` 让闲置 1 小时的桶自动清理；
  4. 令牌够就放行并减一，不够就拒绝。
- **竞态：** 读（HMGET）在事务之外。两个请求同时读到相同的令牌数，都算出"还能放行"，都写回，结果只剩 1 个令牌却放了 2 个请求。MULTI/EXEC 只保证写的几条命令一起执行，不保证"读到的值在写之前没变"。
- **根治：** 把读、算、写整段逻辑放进一个 Lua 脚本，Redis 单线程执行脚本，中间不会插入别的命令。这是争用（contention）的典型解法：把原子边界扩大到整个读改写序列。
- **Redis 的好处：** 亚毫秒响应、EXPIRE 自动清理、可复制做高可用、原子操作。结果是无论第 100 个请求落在哪个网关，看到的都是同一份状态。
