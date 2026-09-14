---
id: runtime-go-lifecycle-graceful-shutdown
node: runtimes.go-lifecycle
type: qa
---
## Q
A new release sends `SIGTERM` and immediately closes the process. What is the correct graceful-shutdown sequence for a streaming edge service?

## A
First become unready so load balancers stop new traffic, while existing connections remain served. Call `Server.Shutdown` with a bounded context, cancel background workers, stop accepting new cache fills, and wait for owned goroutines to exit. After the grace deadline, force-close what remains and record it. Keep the orchestrator termination grace longer than the application's drain budget, or the platform kills the process before cleanup finishes.

## Q zh
新版本收到 `SIGTERM` 后立刻关闭进程。streaming edge service 正确的 graceful-shutdown 顺序是什么？

## A zh
先变为 unready，让 load balancer 停止发送新流量，同时继续服务现有连接。用有界 context 调用 `Server.Shutdown`，取消 background worker，停止接受新 cache fill，并等待 owned goroutine 退出。超过 grace deadline 后再 force-close，并记录数量。orchestrator 的 termination grace 必须长于应用 drain budget，否则平台会在 cleanup 完成前杀进程。
