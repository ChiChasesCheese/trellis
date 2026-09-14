---
id: runtime-go-lifecycle-deadline-budget
node: runtimes.go-lifecycle
type: qa
---
## Q
The edge has 800 ms left before its client deadline, but gives the origin a fresh 2 s timeout. What failure does this create, and how should the timeout be chosen?

## A
The origin keeps working after the edge has abandoned the response, consuming capacity for an answer nobody can use; retries can amplify that waste. Propagate the incoming `Context` and set the origin deadline to the minimum of the remaining budget and the origin policy, minus time reserved for encoding and delivery. Each deeper hop gets a smaller budget, and cancellation must close the response body and stop spawned work.

## Q zh
edge 距离 client deadline 只剩 800 ms，却给 origin 新开了 2 s timeout。它会制造什么故障，timeout 应如何选择？

## A zh
edge 放弃响应后 origin 仍继续工作，为没人能使用的答案消耗容量；retry 会放大浪费。应传播入站 `Context`，origin deadline 取 remaining budget 与 origin policy 的较小值，并预留 encoding 和 delivery 时间。调用链越深，budget 必须越小；cancellation 还必须关闭 response body 并停止衍生工作。
