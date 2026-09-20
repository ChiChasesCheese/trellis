---
id: problems-ride-hailing-ingestion-vs-matching-order-of-magnitude
node: problems.geo.ride-hailing
type: qa
step: 1
tags: [grown]
---
## Q
In a ride-hailing design with 9.7 million monthly drivers, assuming 15% are concurrently online at peak and each sends a location update every 4 seconds, versus roughly 1,389 peak ride-request QPS derived from 40 million trips/day, why does the resulting ~363,750 QPS of location writes force driver location ingestion onto a completely separate pipeline from the ride-matching request path rather than sharing the same transactional flow?

## A
Peak location-update QPS (about 1,455,000 online drivers / 4 seconds ~= 363,750 QPS) is roughly two orders of magnitude higher than peak ride-matching QPS (~1,389), so location ingestion — not matching — is the dominant write load in the whole system. Location updates also have no 'must not be lost' semantics (a dropped update is superseded four seconds later by the next one), so routing them through the same transactional database used for trip records would pay locking and logging costs for a durability guarantee the data doesn't need, while starving the trip database's actual transactional writes under two orders of magnitude more traffic than it was sized for.

## Q zh
在一个网约车设计中，970 万月活司机，假设峰值 15% 同时在线、每人每 4 秒上报一次位置，相比之下由日行程数 4,000 万推算出的峰值叫车请求约 1,389 QPS，为什么由此得到的约 363,750 QPS 位置写入会迫使司机位置摄入走一条和撮合请求路径完全独立的管道，而不是共用同一条事务路径？

## A zh
峰值位置更新 QPS（约 1,455,000 在线司机 / 4 秒 ≈ 363,750 QPS）比峰值撮合请求 QPS（约 1,389）高大约两个数量级，所以位置摄入而不是撮合，才是整个系统里的主负载。位置更新也没有'不能丢'的语义（丢一次，4 秒后的下一次更新自然覆盖），所以把它路由进用于行程记录的同一个事务型数据库，会为一个数据本身用不上的持久性保证付出加锁和写日志的代价，同时让行程数据库真正需要事务保证的写入被淹没在比它设计容量高两个数量级的流量里。
