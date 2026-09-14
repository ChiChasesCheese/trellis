---
id: async-event-time-watermarks
node: async.streaming.processing
type: qa
---
## Q
In stream processing, why window on event time instead of processing time, and what problem do watermarks solve?

## A
**Processing time** windows depend on when data *arrived* — a delayed producer or a replay shifts events into the wrong window and results become non-reproducible. **Event time** windows use timestamps in the data, so results are stable across delays and reprocessing.

But event time forces the question "when is a window complete?" — a **watermark** is the processor's claim that no events older than time T are still coming, letting it close windows. Events arriving after the watermark are *late data*: drop them, or emit corrected/updated window results.

## Q zh
在流处理中，为什么在事件时间而不是处理时间上做窗口，watermark 解决什么问题？

## A zh
**处理时间**窗口取决于数据*何时到达* — 延迟的生产者或重放会把事件推到错误的窗口，结果变得不可重现。**事件时间**窗口使用数据中的时间戳，所以结果在延迟和重处理中保持稳定。

但事件时间强制了一个问题"窗口何时完成？" — **watermark** 是处理器声称不会再有时间 T 之前的事件了，让它关闭窗口。在 watermark 之后到达的事件是*迟到数据*：丢弃它们，或发出修正的/更新的窗口结果。
