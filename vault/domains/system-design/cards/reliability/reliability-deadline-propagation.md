---
id: reliability-deadline-propagation
node: reliability.resilience.retries
type: qa
---
## Q
Service A (1s timeout) calls B, which calls C. C responds in 2s. What goes wrong with naive per-hop timeouts, and what is the fix?

## A
B and C keep doing work for a caller that has **already given up** — wasted capacity, and A may have retried, doubling load. Worse, if inner timeouts are longer than outer ones, errors always surface at the outermost layer, hiding the real culprit.

Fix: **deadline propagation** — the client's remaining budget travels with the request (e.g. gRPC deadlines); each hop subtracts elapsed time and cancels work the moment the deadline is exceeded.

## Q zh
服务 A（1s timeout）调用 B，B 调用 C。C 在 2s 内响应。朴素的 per-hop timeout 有什么问题，修复是什么？

## A zh
B 和 C 为一个已经**放弃**的调用者继续工作——浪费的容量，A 可能已经重试，加倍负载。更坏的是，如果内 timeout 长于外 timeout，错误总是在最外层浮出，隐藏真正的罪魁祸首。

修复：**deadline 传播** ——客户端的剩余预算随请求传走（例如 gRPC deadline）；每个 hop 减去已用时间，在超过 deadline 时立即取消工作。
