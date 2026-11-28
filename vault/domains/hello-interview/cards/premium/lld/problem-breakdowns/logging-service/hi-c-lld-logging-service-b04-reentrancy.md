---
id: hi-c-lld-logging-service-b04-reentrancy
node: lld.problem-breakdowns.logging-service.beyond
type: qa
step: 1
---
## Q
**日志库 · 日志里再打日志：可重入与 fork**｜拓展 · 追问

如果 `Sink.write` 内部（或被它调用的代码）又调用了同一个 logger，会发生什么？fork 出子进程又有什么坑？

## A
- **重入死锁：** 每目的地的锁是不可重入的 `Lock` 时，同一线程在持锁写 sink 的过程中再次进入同一个 `Destination.write`，就会等自己释放，永久死锁。典型情形：sink 里用了会打日志的库（HTTP 客户端、数据库驱动），或信号处理函数里打日志恰好打断了持锁的主线程。
- **应对：** ①用 `RLock`，标准库 `logging.Handler` 就是 RLock；②更稳妥的是让 sink 内部不使用同一个 logger，库自己的诊断走独立通道（stderr）；③信号处理函数里不要直接打日志，设标志位或写管道交给主循环。
- **RLock 的代价：** 允许重入也意味着可能递归写同一个 sink，造成无限递归；要加递归深度保护，或检测到重入就走 stderr 兜底。
- **fork 的坑：** 多线程进程 fork 时，如果别的线程恰好持有日志锁，子进程里那把锁永远处于"已锁定"，而持有它的线程在子进程里不存在，子进程第一次打日志就死锁。Python 的 logging 在 `os.register_at_fork` 里为子进程重新初始化锁，自己写的库需要同样处理，或者避免在多线程后 fork。
