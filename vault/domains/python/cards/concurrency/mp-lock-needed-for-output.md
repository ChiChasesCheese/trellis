---
id: mp-lock-needed-for-output
node: concurrency.multiprocessing
type: qa
source: python-docs
---
## Q
多个进程各自往标准输出 `print()`，为什么输出内容会互相“串行”混杂？如何避免？

## A
多个进程的 `print()` 调用之间没有任何默认的互斥关系，操作系统可能在一次 `print` 的多次底层写调用之间切换到另一个进程执行，导致不同进程的输出字符交错在一起。`multiprocessing` 提供了和 `threading` 同名的同步原语（`Lock`、`RLock`、`Semaphore`、`Event` 等），用一把跨进程共享的 `Lock` 把每个进程的打印包在 `acquire()`/`release()`（或 `with lock:`）之间，就能保证同一时刻只有一个进程在打印，避免交错。
