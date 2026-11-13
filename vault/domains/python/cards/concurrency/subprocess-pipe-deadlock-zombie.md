---
id: subprocess-pipe-deadlock-zombie
node: concurrency.multiprocessing
type: qa
---
## Q
`p = Popen(cmd, stdout=PIPE); p.wait()` 在子进程输出很多时会永远卡住，为什么？僵尸进程（zombie）是什么，在 Python 里什么情况下会产生？

## A
**管道（pipe）有固定容量（Linux 默认 64 KiB）。子进程写满后阻塞在 `write` 上等你读；你却在 `wait()` 里等它退出。双方互等，就是死锁。**

```python
p = Popen([sys.executable, "-c", "print('x' * 200_000)"], stdout=PIPE)
p.wait(timeout=2)            # 实测：2 秒后 TimeoutExpired，子进程卡在写管道
out, _ = p.communicate()     # 边读边等：拿到 200001 字节，returncode 0
```

- **正确做法：** 用 `communicate()`（或 `run`），它同时读 stdout 和 stderr 直到 EOF，再回收进程。需要实时处理输出时，逐行读 `p.stdout`，并把 stderr 合并进 stdout（`stderr=STDOUT`）或另开线程读，否则 stderr 那根管道照样会满。
- **只捕获 stdout 也会卡：** 如果 stdout 被读而 stderr 设成 `PIPE` 却没人读，子进程往 stderr 写满 64 KiB 一样会卡住。
- **僵尸进程：** 子进程已经退出，但父进程还没调用 `wait` 读取它的退出状态，内核只好保留它的进程表项，`ps` 里状态显示为 `Z`。它不占 CPU 和内存，但占 PID；大量积累会耗尽 PID。实测：`Popen(["true"])` 后不调用 `wait`，0.5 秒后 `ps` 显示 `Z`；`p.wait()` 之后这一项消失。
- **Python 里怎么产生：** `Popen` 了却从不 `wait` / `communicate` / `poll`。如果 `Popen` 对象被垃圾回收时子进程还在运行，CPython 会把它记下来，等之后创建新的 `Popen` 时顺手回收，但不能依赖它；长期运行的测试调度器应当显式回收每个子进程。
- **孤儿进程（orphan）不同：** 父进程先死，子进程还在跑，会被 init（PID 1）或设置了 subreaper 的进程收养并最终回收。容器的 PID 1 如果是不回收子进程的普通程序，孤儿退出后就会变成僵尸积累，所以容器里常用 `tini` 或 `docker run --init` 做 PID 1。
