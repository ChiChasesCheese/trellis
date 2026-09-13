---
id: dist-retries-budget
node: distributed.retries
type: qa
---
## Q
Three service layers each retry three times. How can one user request become a dependency outage amplifier?

## A
Independent retries multiply: four attempts at three layers can create `4^3 = 64` calls at the bottom. Retry at one owning layer, cap total attempts and elapsed budget, use exponential backoff with jitter, and honor server overload signals. Track retry ratio and spend from a shared retry budget. A retry is extra load issued when the dependency is already signaling trouble.

## Q zh
三层 service 各自 retry 三次。一次 user request 如何变成 dependency outage amplifier？

## A zh
独立 retry 会相乘：三层各四次 attempt，底层可收到 `4^3 = 64` 次调用。只让一个 owning layer retry，限制 total attempts 和 elapsed budget，使用带 jitter 的 exponential backoff，并遵守 server overload signal。跟踪 retry ratio，并从共享 retry budget 消耗。retry 是 dependency 已在报错时施加的额外负载。
