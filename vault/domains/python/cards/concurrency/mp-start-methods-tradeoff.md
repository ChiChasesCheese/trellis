---
id: mp-start-methods-tradeoff
node: concurrency.multiprocessing
type: qa
source: python-docs
---
## Q
`multiprocessing` 的三种启动方式 `spawn`、`fork`、`forkserver` 在“子进程继承什么”和“启动速度”上分别有什么区别？

## A
`fork` 用 `os.fork()` 复制父进程，子进程一开始和父进程几乎完全一样（继承所有资源），启动最快，但在多线程父进程里不安全（只会复制发起 fork 的那个线程，其他线程持有的锁状态可能不一致，导致死锁）。`spawn` 启动一个全新的 Python 解释器进程，只继承运行目标函数必需的资源，更安全但启动明显慢于 fork。`forkserver` 先启动一个单线程的服务进程，之后每次需要新进程就让这个服务进程去 fork，兼顾了 fork 的速度和“发起 fork 的进程是单线程”的安全性。
