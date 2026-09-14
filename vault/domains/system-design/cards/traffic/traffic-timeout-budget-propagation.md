---
id: traffic-timeout-budget-propagation
node: traffic.gateways
type: qa
---
## Q
The gateway times out at 10 s, but a service it calls uses a 15 s timeout on its own downstream call. What goes wrong, and what discipline fixes it?

## A
After 10 s the gateway returns 504 and the client may retry — while the abandoned request **keeps computing downstream** for 5 more seconds. Under overload this wasted work compounds: the system burns capacity on answers nobody will receive, stacked under fresh retries.

Fix: **deadline propagation** — attach the remaining budget to the request (gRPC deadlines, a budget header); every hop sets its timeout to ≤ what remains minus its own work, and cancels downstream calls when its caller gives up.

Rule: timeouts must strictly shrink as you go deeper in the call tree.

## Q zh
网关在 10 秒超时，但一个服务它调用在它自己的下游调用使用 15 秒超时。什么出错了，什么纪律修复它？

## A zh
10 秒后网关返回 504 并且客户端可能重试 — 当被遗弃的请求**继续计算下游**5 秒。在过载下这个浪费工作复合：系统在没人会收到的答案上燃烧容量，堆积在新重试下。

修复：**截止传播** — 将剩余预算附加到请求（gRPC 截止、预算头）；每个跳跃将其超时设置为 ≤ 剩余减去其自己的工作，并在其调用者放弃时取消下游调用。

规则：当你在调用树中深入时超时必须严格缩小。
