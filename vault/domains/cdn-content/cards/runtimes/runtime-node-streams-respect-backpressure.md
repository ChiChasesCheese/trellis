---
id: runtime-node-streams-respect-backpressure
node: runtimes.node-streams
type: qa
---
## Q
A Node proxy calls `writable.write(chunk)` in a loop and ignores its return value. What happens with slow clients, and what is the correct pattern?

## A
When `write()` returns `false`, the internal buffer has crossed `highWaterMark`. Continuing to write accumulates unbounded memory and increases GC and tail latency. Pause the producer until `'drain'`, or use `stream.pipeline()` so backpressure and error teardown propagate automatically. `highWaterMark` is a buffering threshold, not a hard memory cap, so upstream production must actually stop.

## Q zh
Node proxy 在循环中调用 `writable.write(chunk)`，却忽略返回值。slow client 下会发生什么，正确模式是什么？

## A zh
当 `write()` 返回 `false`，internal buffer 已越过 `highWaterMark`。继续写会积累无界内存，增加 GC 和 tail latency。应暂停 producer，等待 `'drain'`，或使用 `stream.pipeline()` 自动传播 backpressure 与 error teardown。`highWaterMark` 是 buffering threshold，不是硬性 memory cap，因此 upstream production 必须真正停止。
