---
id: runtime-openresty-nonblocking-io
node: runtimes.lua-openresty
type: qa
---
## Q
An OpenResty access hook uses a blocking Lua socket library for policy lookup. Why can one slow call stall many requests, and what API model is required?

## A
Each Nginx worker runs an event loop. Blocking foreign I/O holds the worker thread, so unrelated connections assigned to that worker cannot progress. Use OpenResty cosocket APIs, which yield the request coroutine while Nginx waits for readiness; set connect/read/write timeouts and reuse connection pools. If a library cannot integrate with cosockets, move it outside the request hot path or to another service.

## Q zh
OpenResty access hook 用 blocking Lua socket library 查询 policy。为什么一个 slow call 会拖住许多请求，需要什么 API model？

## A zh
每个 Nginx worker 都运行一个 event loop。blocking foreign I/O 会占住 worker thread，使分配给该 worker 的无关连接也无法前进。应使用 OpenResty cosocket API：等待 readiness 时 yield request coroutine；同时设置 connect/read/write timeout 并复用 connection pool。若 library 无法接入 cosocket，就把它移出 request hot path 或放到独立服务。
