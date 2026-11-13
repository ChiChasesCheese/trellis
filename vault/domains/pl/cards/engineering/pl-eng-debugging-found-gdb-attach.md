---
id: pl-eng-debugging-found-gdb-attach
node: engineering.debugging
type: qa
step: 13
---
## Q
一个测试里的原生进程卡住了，没有崩溃，所以没有核心转储。怎么用 gdb 附加（attach）到正在运行的进程上看它卡在哪里？附加会对进程造成什么影响，容器里为什么常常附加不上？

## A
**`gdb -p <PID>` 附加后进程会被暂停，你看完栈后 `detach`，进程从原处继续。如果只想留一份现场带走，用 `gcore` 生成核心转储而不杀死进程。**

```text
$ gdb -p 4242
(gdb) thread apply all bt        # 每个线程卡在哪：锁、条件变量、系统调用
(gdb) detach                     # 放开，进程继续运行
(gdb) quit

$ gcore -o /tmp/hang 4242        # 写出 /tmp/hang.4242，进程继续运行
$ gdb -batch -p 4242 -ex 'thread apply all bt' > hang.txt   # 一条命令导出
```

- **附加的影响：** 附加期间进程完全停住，持有的锁不释放、心跳停止，线上服务可能被健康检查判定死亡并重启。所以动作要快，或者用 `gcore` 留现场再到别处慢慢看。
- **怎么读卡死的栈：** 多个线程停在 `pthread_mutex_lock` 或 `futex` 等待，说明在等锁，再看是谁持有；停在 `read`、`recv`、`epoll_wait`，说明在等 I/O 或对端；只有一个线程在跑、栈每次都不同，那是死循环而不是卡死。隔几秒抓两三次，对比哪些栈一直不变。
- **为什么附加不上：**
  - Linux 的 Yama 安全模块：`/proc/sys/kernel/yama/ptrace_scope` 为 1 时，普通用户只能附加到自己的子进程，要用 `sudo` 或有 `CAP_SYS_PTRACE` 能力。
  - 容器默认没有这个能力，要 `docker run --cap-add=SYS_PTRACE`；Kubernetes 里用 `kubectl debug` 起一个带调试工具的临时容器。
  - 同一时刻一个进程只能被一个跟踪者附加：如果它已经在 `strace` 下运行，gdb 就附加不上。
- **Python 进程：** 优先用 `py-spy dump --pid <PID>`，它从外部读取内存，不需要暂停太久，直接打印 Python 层各线程的栈；需要看 C 层时再用 gdb 加 `py-bt`。
- **Java 和 Go：** Java 用 `jcmd <PID> Thread.print`，Go 用 `/debug/pprof/goroutine?debug=2`，都比 gdb 更懂各自的运行时。
