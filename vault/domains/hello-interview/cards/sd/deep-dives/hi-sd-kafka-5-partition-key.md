---
id: hi-sd-kafka-5-partition-key
node: qb.sd.job-scheduler-cron-history.pre-sd-deep-dives-kafka
type: qa
step: 5
---
## Q
**分区策略与热点分区**｜系统设计 · 深入技术

扩展 Kafka 时面试里应该先谈什么？分区号怎么算？广告点击按 ad id 分区遇到爆款广告变成热分区，有哪些办法？

## A
**扩展。** 加 broker 要保证 topic 的分区足够多，否则新 broker 用不上（分区不足）。真正该谈的是分区键：`partition = hash(key) % num_partitions`（默认 murmur2）。键选得好，数据均匀；选坏了就出现热点分区。

**热点的办法。**
- 不设 key：默认粘性（sticky）分区器批量写一个分区再轮换，大致均匀；代价是丢失同 key 的顺序保证
- 随机加盐（salting）：在 ad id 后拼随机数，分散负载，但消费端聚合更复杂
- 复合键：ad id 加地区或用户段等相互独立的属性
- 背压（back pressure）：生产者检查分区滞后，过高就放慢

**说法。** 面试中讨论性能，几乎总是从分区策略开始。
