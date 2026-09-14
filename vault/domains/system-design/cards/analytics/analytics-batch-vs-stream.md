---
id: analytics-batch-vs-stream
node: analytics.batch
type: qa
---
## Q
What is the real boundary between batch and stream processing, and how does each recover from failure?

## A
The input: batch reads a **bounded** dataset of known size (job can finish, sort, and take multiple passes); streaming reads an **unbounded** log and must produce results incrementally, forcing explicit handling of time — windows, watermarks, late events.

Recovery differs accordingly:
- **Batch**: throw away partial output, rerun the job — cheap because inputs are immutable and outputs atomic (see [[analytics-idempotent-reruns]]).
- **Stream**: can't replay from the beginning of time forever, so recover from periodic **checkpoints of operator state + log offsets**, replaying only since the last checkpoint.

Microbatching (Spark Structured Streaming) and unified engines blur the API, not this recovery distinction.

## Q zh
batch 和 stream 处理之间的真正边界是什么，每个如何从故障恢复？

## A zh
输入：batch 读一个**有限**的已知大小数据集（job 可以完成、排序、多次遍历）；stream 读一个**无限**日志且必须增量产生结果，强制显式处理时间 — 窗口、watermark、迟到事件。

恢复相应不同：
- **Batch**：丢弃部分输出，重新运行 job — 便宜，因为输入不可变和输出原子。
- **Stream**：无法永远从时间开始重放，所以从定期**operator state + log offset 的 checkpoint**恢复，仅从最后 checkpoint 后重放。

Microbatching（Spark Structured Streaming）和统一引擎模糊 API，不是这个恢复区别。
