---
id: threads-daemon-exit
node: concurrency.threads
type: qa
source: python-docs
---
## Q
把一个线程标记为守护线程（daemon thread）会改变程序的退出行为吗？

## A
会。当进程里只剩守护线程存活时，整个 Python 程序会直接退出，不等待这些守护线程运行完毕，它们被“粗暴地”终止，持有的资源（打开的文件、数据库事务等）可能得不到正确释放。非守护线程默认继承自创建它的线程；若希望线程能优雅退出，应保持非守护并用 `Event` 等信号机制主动通知其结束，而不是依赖守护标记。
