---
id: hi-c-sd-redis-n14-streams
node: sd.deep-dives.redis.notes
type: qa
step: 13
---
## Q
**Redis · 流与事件溯源、工作队列**｜摘要 · 必会

Redis 流怎么做工作队列？worker 死掉怎么办？什么时候该换 Kafka？

## A
- **流（stream）：** 追加式日志，类似 Kafka 的主题，是事件溯源（保存事件顺序日志，由它推导状态）的构件。`XADD` 追加，消费者组（`XREADGROUP`、`XCLAIM`）协调谁处理哪条。
- **工作队列：** 用 `XADD` 入队，给流挂一个消费者组供 worker 使用。正常路径是 worker 用 `XREADGROUP` 读一条、处理、确认。消费者组记录每条待处理项交给了谁，以及它的空闲时间。
- **worker 中途死掉：** 它那条待处理项的空闲时间一直增长，直到别的 worker 用 `XCLAIM` / `XAUTOCLAIM` 接手并重跑。这也意味着一条消息偶尔会被处理两次（Redis 分不出慢和死），所以处理逻辑要幂等。
- **耐久性提醒：** 流条目只有持久化设置那么耐久，默认设置下崩溃可能丢最近的条目。
- **什么时候用 Kafka：** 流适合设计里已经有 Redis、队列体量不大（后台任务、通知扇出、任务分发）；需要长保留、让很多独立消费者回放、规模大到不能丢消息的有序吞吐时，Kafka 才值得它的运维复杂度。
