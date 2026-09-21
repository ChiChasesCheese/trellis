---
id: mp-314-default-forkserver
node: concurrency.multiprocessing
type: qa
source: python-docs
---
## Q
Python 3.14 把 POSIX 平台上 `multiprocessing` 的默认启动方式从什么改成了什么？为什么？

## A
从默认 `fork` 改成默认 `forkserver`。原因是 `fork` 在多线程程序里不安全：子进程只复制发起 `os.fork()` 的那个线程，其余线程持有的锁、正在进行的系统调用等状态不会被正确复制，容易导致子进程里的死锁或崩溃。`forkserver` 由一个专门维护的单线程服务进程去执行实际的 fork，既保留了接近 fork 的启动速度，又避免了对多线程父进程做 fork 的隐患。Windows 和 macOS 的默认启动方式仍是 `spawn`（macOS 自 3.8 起如此）。
