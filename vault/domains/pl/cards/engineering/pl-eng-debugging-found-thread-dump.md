---
id: pl-eng-debugging-found-thread-dump
node: engineering.debugging
type: qa
step: 3
---
## Q
服务卡住、死锁、请求超时时，线程转储（thread dump）能告诉你什么？Java 的 `jcmd Thread.print` 和 Go 的 `SIGQUIT` 各是什么样子？

## A
**线程转储**是“此刻每个线程/协程在哪一行、在等什么”的快照。卡死类问题的根因几乎总是在这里：大家都在等同一把锁、同一个下游调用、同一个连接池。抓两三次，看哪些栈**一直没变**。

**Java**：`jcmd <pid> Thread.print`（或 `jstack`）不需要重启，也不中断服务。两个线程以相反顺序拿锁的死锁，输出直接给出诊断：
```
Found one Java-level deadlock:
"worker-1":
  waiting to lock monitor ... (a java.lang.Object),
  which is held by "worker-2"
"worker-2":
  waiting to lock monitor ... (a java.lang.Object),
  which is held by "worker-1"
```
JVM 会自动检测“锁等待环”并指出线程名与代码行。

**Go**：给进程发 `SIGQUIT`（`kill -QUIT <pid>`）会打印所有 goroutine 的栈并退出（崩溃式）；线上更常用 `net/http/pprof` 的 `/debug/pprof/goroutine?debug=2`，不会杀进程。一个卡在下游调用的程序，转储里是：
```
goroutine 1 [sync.WaitGroup.Wait]:
sync.(*WaitGroup).Wait(...)
goroutine 19 [sleep]:
main.fetch(...)
```
方括号里是 goroutine 此刻的等待原因（`chan receive`、`sleep`、`select`、`semacquire`……），这是最有用的信息。如果程序里**所有** goroutine 都在等，运行时会主动报：`fatal error: all goroutines are asleep - deadlock!`，并打印每个 goroutine 的栈。

**Python**：`faulthandler.dump_traceback_later(timeout)` 或 `kill -SIGUSR1`（配合 `faulthandler.register`）打印所有线程的栈；在不能改代码的进程上，用 `py-spy dump --pid <pid>` 从外部读取。**Rust**：附加 `lldb`/`gdb` 后用 `thread backtrace all`；`async` 任务没有线程栈，要用 `tokio-console` 看任务状态。

**读转储的方法**：先看“有多少线程停在同一个位置”，再看它们在等的对象被谁持有。一个数百线程都停在 `getConnection()` 的服务，问题是连接池耗尽，而不是代码慢。
