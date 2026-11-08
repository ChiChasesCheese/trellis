---
id: hi-sd-tinder-3-hld-swipe
node: sd.problem-breakdowns.tinder.exam
type: qa
step: 3
---
## Q
**Tinder：高层设计与滑动服务拆分**｜系统设计 · 问题拆解

Tinder 的高层设计里，为什么把滑动服务（Swipe Service）和数据库从资料服务里拆出来？滑动数据该用什么库、怎么分区？

## A
**基础流程。** 客户端 -> API Gateway -> Profile Service -> 用户库，处理资料创建和 feed 查询（先用简单的范围查询，后面再优化）。

**为什么拆。** 看资料和建资料的频率远低于滑动写入，拆开后滑动服务可独立扩容、独立做缓存策略。数据量也不同：2000 万日活 × 100 次 × 每条约 100 字节 ≈ 200GB / 天，需要分区和写优化的存储。

**选 Cassandra。** 它的写入路径是 commit log、memtable、SSTable，写吞吐大。以 swiping_user_id 为分区键，"A 是否滑过 B" 只需查一个分区，速度可预测。

**代价。** Cassandra 的滑动数据只有最终一致，会让"双方同时右滑"的检测出问题，需要专门解决。

**匹配检查。** 写入滑动后，查对方是否已对自己右滑，有就返回匹配。
