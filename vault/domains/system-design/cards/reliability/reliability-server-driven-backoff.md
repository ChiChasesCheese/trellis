---
id: reliability-server-driven-backoff
node: reliability.resilience.retries
type: qa
---
## Q
Every client is individually well-behaved (exponential backoff + jitter, 3 attempts) and the service is still being retried into the ground. Why, and what two mechanisms fix it?

## A
Client-side backoff is **local knowledge**: each client only sees its own failures, so it cannot know that 10k other clients are backing off against the same overloaded server. The aggregate retry rate is still far above what the server can absorb, and the server pays CPU to reject each one.

- **Server-driven backoff**: reply `429`/`503` with **`Retry-After`** (or a gRPC push-back / throttling hint) — the server is the only party that knows the real recovery time, and it can spread clients by returning jittered values. Rejects must be *cheap* (shed at the edge before touching the DB) or the rejection path becomes the outage.
- **Adaptive client throttling** (Google SRE): each client tracks `requests` and `accepts` over ~2 minutes and drops its own requests with probability `max(0, (requests − K·accepts) / (requests + 1))`, K≈2. As the server's accept rate falls the client self-limits, so the retry load converges to roughly what the server can serve — a client-side circuit breaker with a knob instead of a switch.

Both are the enforcement mechanism behind a **retry budget** (e.g. retries ≤ 10% of requests), which is otherwise just an unenforced intention.

## Q zh
每个客户端单独表现良好（指数退避 + 抖动，3 次尝试）服务仍然被重试到地面。为什么，什么两个机制修复它？

## A zh
客户端退避是**本地知识**：每个客户端只看到自己的失败，所以它无法知道 10k 其他客户端对同一过载服务器退避。聚合重试率仍然远高于服务器可以吸收，服务器支付 CPU 拒绝每一个。

- **服务器驱动退避**：回复`429`/`503`带**`Retry-After`**（或 gRPC 推回 / 节流提示）——服务器是唯一知道真实恢复时间的方，可以通过返回抖动值来传播客户端。拒绝必须*便宜*（在触及 DB 之前在边缘移除）或拒绝路径变成停机。
- **自适应客户端节流**（Google SRE）：每个客户端在 ~2 分钟内跟踪`requests`和`accepts`并以概率`max(0, (requests − K·accepts) / (requests + 1))`丢弃自己的请求，K≈2。当服务器的接受率下降时客户端自我限制，所以重试负载收敛到大约服务器可以服务——一个带旋钮而不是开关的客户端 circuit breaker。

两者都是**retry budget**后面的强制机制（例如重试 ≤ 10% 的请求），否则只是无强制意图。
