---
id: concurrency-producer-consumer-queue
node: concurrency.patterns
type: qa
step: 1
---
## Q
用标准库实现一个生产者-消费者（producer-consumer）模型，默认应该选哪个工具，为什么不用自己拿 `Lock` 手搓？

## A
默认选 `queue.Queue`：它已经把"有元素才能取、没满才能放、多生产者多消费者并发访问"这些同步逻辑封装好了，`put()`/`get()` 本身就是线程安全且会正确阻塞的。

```python
import threading, queue

q = queue.Queue(maxsize=100)

def producer():
    for item in work_items():
        q.put(item)  # 满了自动阻塞

def consumer():
    while True:
        item = q.get()  # 空了自动阻塞
        process(item)
        q.task_done()
```

自己用 `Lock` 手搓等价物意味着要重新发明"空/满时阻塞、多个等待者互不踩踏、避免丢信号"这些已经被标准库踩过坑、测试过的边界情况——除非需求超出了 `Queue` 的接口（比如要窥视队首、要按优先级出队且没有现成实现），否则没有理由自己写。
