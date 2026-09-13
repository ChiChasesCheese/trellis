---
id: fnd-io-fd-exhaustion
node: foundations.os-io
type: qa
---
## Q
A proxy still has spare CPU, but new connections fail with `EMFILE`. What is exhausted, what usually leaks it, and what must you inspect?

## A
The process hit its **file descriptor limit**. Every accepted socket, upstream connection, file, and pipe consumes an FD; missing closes, unbounded keep-alive pools, or too-low limits cause exhaustion. Inspect `/proc/<pid>/fd`, socket states, connection-pool bounds, process `ulimit`, and close paths. Raising the limit only delays a leak.

## Q zh
proxy 的 CPU 还有余量，但新连接报 `EMFILE`。耗尽的是什么，常见泄漏源是什么，应该检查什么？

## A zh
进程撞到了 **file descriptor limit**。每个 accepted socket、upstream connection、文件和 pipe 都占用一个 FD；漏掉 close、无界 keep-alive pool 或过低 limit 都会耗尽它。检查 `/proc/<pid>/fd`、socket state、connection-pool bound、进程 `ulimit` 和所有 close path。单纯提高 limit 只会推迟 leak。
