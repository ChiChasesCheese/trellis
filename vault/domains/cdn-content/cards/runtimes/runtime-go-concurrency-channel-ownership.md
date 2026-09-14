---
id: runtime-go-concurrency-channel-ownership
node: runtimes.go-concurrency
type: qa
---
## Q
Two producers may close the same result channel when either finishes. Production occasionally panics with `close of closed channel`. What ownership rule fixes this?

## A
Only the goroutine that owns channel creation and knows no more sends can occur should close it. Producers send and return; a coordinator waits for all producers, then closes once. Receivers normally do not close channels. Closing is a lifecycle signal, not cleanup that every participant should attempt. If cancellation is the goal, cancel a shared `Context` rather than racing to close a data channel.

## Q zh
两个 producer 都可能在完成时关闭同一个 result channel，生产偶发 `close of closed channel` panic。什么 ownership 规则能修复？

## A zh
只有创建 channel、并且能确定以后不会再发送的 goroutine 才应关闭它。producer 只发送然后退出；coordinator 等待所有 producer 完成后关闭一次。receiver 通常不关闭 channel。close 是 lifecycle signal，不是每个参与者都要尝试的 cleanup。若目标是 cancellation，应取消共享 `Context`，而不是争抢关闭 data channel。
