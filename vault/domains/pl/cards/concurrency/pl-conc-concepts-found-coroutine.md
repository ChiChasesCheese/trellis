---
id: pl-conc-concepts-found-coroutine
node: concurrency.concepts
type: qa
step: 3
---
## Q
协程（coroutine）是什么？它和线程的调度方式有什么不同，什么叫“协作式”并发？

## A
**协程**是一种可以在中途**暂停**、之后从暂停处**继续**的函数。线程由操作系统在任意时刻强行打断（**抢占式**调度），协程只在自己主动让出的位置暂停（**协作式**调度），由程序里的“调度器”决定下一个跑谁。

心智模型：几个人共用一台电脑，规则是“用完一段就自觉把键盘交给下一个”。没有人会在你敲到一半时被抢走键盘，所以两个任务不会在同一行代码中间交错；但如果有人一直不交出去，其他人就永远等着。

一个用 Python 生成器模拟的最小调度器：
```python
def task(name, steps):
    for i in range(steps):
        print(f"{name} step {i}")
        yield                      # hand control back to the scheduler

tasks = [task("A", 3), task("B", 2)]
while tasks:
    for t in list(tasks):
        try: next(t)
        except StopIteration: tasks.remove(t)
```
输出：`A step 0`、`B step 0`、`A step 1`、`B step 1`、`A step 2`。两个任务在**同一个线程**里交替前进，`yield` 就是让出点；B 先跑完被移出，A 单独跑完最后一步。

协程的特点：
1. 切换只是在用户态保存和恢复少量状态，比线程切换便宜得多，所以可以开几十万个；
2. 因为让出点是显式的，不需要锁保护让出点之间的代码（但跨让出点的共享状态仍然要小心）；
3. 一个任务做长时间的计算或阻塞调用，会卡住同一调度器上的所有协程；
4. 单个协程不能同时用多个核，要用多核得有多个调度线程。

goroutine、虚拟线程、`async/await` 都是协程思想的不同实现：谁调度、能否抢占、有没有栈、需不需要标记函数。
