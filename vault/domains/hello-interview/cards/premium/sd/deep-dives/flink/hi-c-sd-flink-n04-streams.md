---
id: hi-c-sd-flink-n04-streams
node: sd.deep-dives.flink.notes
type: qa
step: 4
---
## Q
**Flink · 流：无界序列，持久性靠检查点**｜摘要 · 必会

Flink 的流和 Kafka 的主题是一回事吗？

## A
- **流（stream）：** 无界的数据元素序列，像一个无限长的事件数组，每个事件如 `{user_id, action, timestamp, page}`。
- **能做什么：** Flink 提供切分、转换、聚合、重组等工具处理它。
- **不等于 Kafka 主题：** Flink 的流不一定是追加日志，没有偏移量（offset），也不要求持久保存。
- **持久性靠检查点：** 耐久性由系统定期创建的检查点（checkpoint）来保证，而不是流本身保存数据。
- **所以：** 恢复时要靠可重读的源（Kafka）配合检查点，而不是靠流自己重放。
