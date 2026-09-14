---
id: net-proxy-timeout-budget
node: networking.proxies
type: qa
tags: [grown]
---
## Q
A reverse proxy has no timeout of its own for waiting on a response — it simply waits as long as the upstream takes. One upstream starts responding slowly under load, without erroring. What happens to the proxy as this continues, and why does the proxy need a timeout distinct from any timeout the upstream enforces on itself?

## A
Each slow request holds open one of the proxy's own connections, worker threads, or pooled sockets while it waits. As concurrent slow requests accumulate, the proxy exhausts its own finite connection or thread capacity and stops accepting new requests **for every upstream**, not just the slow one — a localized slowdown becomes a proxy-wide outage. A proxy-side timeout, set shorter than the proxy can tolerate holding a resource open, bounds how long any single request may occupy proxy capacity: on expiry the proxy releases the resource and returns an error response (for example, `504 Gateway Timeout`) instead of waiting indefinitely, which decouples the proxy's own health from any one upstream's latency.

## Q zh
一个 reverse proxy 自己没有等待响应的 timeout——它只是耐心等 upstream 需要多久就等多久。某个 upstream 在负载下开始响应变慢，但没有报错。这种情况持续下去，proxy 会发生什么？为什么 proxy 需要一个独立于 upstream 自身 timeout 的 timeout？

## A zh
每个慢请求都会占住 proxy 自己的一个 connection、worker 线程或连接池里的一个 socket，直到等到响应为止。随着并发的慢请求不断累积，proxy 会耗尽自己有限的 connection 或线程容量，从而**对所有 upstream**都停止接受新请求，而不只是那个变慢的 upstream——一次局部的性能下降就变成了整个 proxy 层面的中断。proxy 侧的 timeout（设置得比 proxy 能承受的资源占用时长更短）限定了任何单个请求最多能占用多久 proxy 容量：一旦超时，proxy 就释放这个资源并返回一个错误响应（比如 `504 Gateway Timeout`），而不是无限期等待，这样就把 proxy 自身的健康状况和任何单个 upstream 的延迟解耦开了。
