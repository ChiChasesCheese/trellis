---
id: lcp-rate-limiter-reflection-multi-instance
node: lcproject.lcp-rate-limiter
type: qa
step: 12
tags: [作答]
---
## Q
LLM 网关限流器的项目要你写第二段反思：网关从一台机器扩到二十台、前面加了负载均衡，限流状态不能再放在各自的内存里。设计要怎么改？如果把状态放进 Redis，哪几步必须仍然是原子的，又多出了哪些新问题？

## A
**评分点**
- 说出状态外移到共享存储，读、判、写必须仍是一个原子步骤
- 说出 Redis 用 Lua 脚本（EVAL）或 MULTI/WATCH；Memcached 只能靠 cas 重试，竞争高时重试多
- 说出时钟：用存储服务端的时间，避免各实例时钟漂移让窗口错位
- 说出过期：key 设 TTL（窗口长度或补满所需时间），代替本地回收
- 说出代价：每个请求多一次网络往返，存储成为新的故障点，要决定 fail open 还是 fail closed
- 说出折中：本地预取一部分额度、定期与中心对账；统计改写入共享计数器

<details class="pt"><summary>参考答案</summary>

把字典换成共享存储，但"读—判—写"不能拆开：Redis 里用 Lua 脚本在服务端一次执行（滑动窗口用有序集合存时间戳，令牌桶存令牌数与时间戳），Memcached 靠 `cas` 重试。时钟取存储服务端的，key 设 TTL 代替回收。每个请求多一次网络往返，存储不可用时要决定放行还是拒绝；可本地预取额度折中，统计写入共享计数器。

</details>

**知识点：** 线程安全结构的写法（Thread-Safe Structures）、内存持久化（In-Memory Persistence）、重试与退避（Retry & Backoff）
