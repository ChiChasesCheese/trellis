---
id: hi-pt-elevator-design-9-testable
node: qb.lld.elevator-design.points
type: qa
step: 9
---
## Q
**电梯系统 · 可测试的时钟与高峰优化**｜出自：电梯系统 › 取舍与追问

追问：怎么测电梯的停靠顺序？高峰期怎么优化？

## A
**测试。** 时间由 `tick` 驱动，不依赖真实睡眠，可脚本化按键并断言停靠顺序；例如电梯在 0 层、轿厢内选 9、7 层有下行呼叫、2 层有上行呼叫，结果顺序是 2、9、7。
**高峰。** 上班高峰空闲时把电梯预先停在大堂，下班反之。
**Java。** 请求队列用 `BlockingQueue`，`ScheduledExecutorService` 每个时间片调用一次 `tick`。
