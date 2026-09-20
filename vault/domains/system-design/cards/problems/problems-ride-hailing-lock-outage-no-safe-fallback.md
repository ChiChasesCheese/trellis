---
id: problems-ride-hailing-lock-outage-no-safe-fallback
node: problems.geo.ride-hailing
type: qa
step: 6
tags: [grown]
---
## Q
In a ride-hailing matching service, when the distributed lock store used for driver exclusivity becomes unavailable, why is queuing matching requests until the lock store recovers the correct response, rather than falling back to matching without a lock?

## A
Falling back to lock-free matching to keep availability up would reintroduce the exact race condition the lock exists to prevent — two concurrent requests could both select and invite the same driver, producing a duplicate-booking bug the user directly experiences. Unlike other components in this design (like the location store, where falling back to a slightly stale position is an acceptable degradation), there is no safe degraded mode for the exclusivity guarantee itself, so the correct response is to accept a temporary increase in matching latency by queuing requests until the lock store is healthy again, rather than trading away correctness for availability.

## Q zh
在一个网约车撮合服务中，当用于司机排他性的分布式锁存储不可用时，为什么正确的应对是把撮合请求排队等待锁存储恢复，而不是退回到不加锁直接撮合？

## A zh
为了保住可用性而退回到无锁撮合，会重新引入锁本来要防止的那个竞态条件——两个并发请求完全可能同时选中并邀请同一个司机，产生一个用户能直接感知到的重复绑定 bug。和这个设计里其他组件不同（比如位置存储，退回到稍微陈旧的位置是可以接受的降级），排他性这个保证本身没有安全的降级模式，所以正确的应对是接受撮合延迟暂时变长、把请求排队等到锁存储恢复健康，而不是用正确性换可用性。
