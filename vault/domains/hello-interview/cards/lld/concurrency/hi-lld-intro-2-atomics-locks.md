---
id: hi-lld-intro-2-atomics-locks
node: lld.concurrency.intro
type: qa
step: 2
---
## Q
**原子变量与锁**｜低层设计 · 并发

原子变量（atomics）和锁（mutex）各解决什么？什么时候原子变量不够用？Python 里怎么办？

## A
**要点。** 原子变量对单个变量提供无锁的线程安全操作，底层用比较并交换（CAS）这类一步完成、不可打断的 CPU 指令。适合计数器、标志位、简单统计，又快又受限于单个变量：一旦要同时更新两个东西，原子变量就帮不上了。

锁提供互斥：持锁线程在临界区内执行，其他想获取的线程阻塞，直到释放。它是保护共享状态的默认工具。变体有粗粒度（一把锁管全部）、细粒度（每个资源一把锁）、读写锁（多读或单写）。

**易错。** Python 没有原生原子变量，递增共享计数器也要加锁。

```python
import threading

lock = threading.Lock()
counter = 0

def increment() -> None:
    global counter
    with lock:           # 读、改、写作为整体，其他线程不能插入
        counter += 1
```

**使用时机。** 单变量的读改写用原子变量；先检查后操作、多字段更新用锁。
