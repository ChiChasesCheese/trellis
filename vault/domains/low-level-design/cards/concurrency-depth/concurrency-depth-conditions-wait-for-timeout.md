---
id: concurrency-depth-conditions-wait-for-timeout
node: concurrency-depth.conditions
type: qa
step: 2
---
## Q
给一个取任务的方法加 1 秒超时。有人写 `while not items: cond.wait(timeout=1)`，有人写 `cond.wait_for(lambda: items, timeout=1)`。两种写法的超时分别是什么意思？超时返回时，怎么知道谓词成立没有？

## A
**要总期限和结果，用 `wait_for`**

- **手写循环的超时是“每一轮”**：每次被唤醒又发现条件不成立，就重新等一个完整的 1 秒；不断有无关的通知，总等待可以远超 1 秒；
- **`wait_for` 的超时是总期限**：它按单调时钟算出截止时间，每轮只等剩下的时间；
- **`wait()` 的返回值不说明谓词**：超时返回 `False`，被通知返回 `True`，但被通知后条件可能已被别人抢走；
- **`wait_for` 返回谓词最后一次的值**：`False` 就是超时且条件不成立，调用方据此抛 `TimeoutError`；
- **超时后锁仍然是持有的**：`wait` 和 `wait_for` 返回前都会重新拿回锁，所以取走元素的代码可以紧跟其后。

```python
import threading, time
cond, items = threading.Condition(), []
def take(timeout):
    with cond:
        if not cond.wait_for(lambda: items, timeout):   # False：超时且仍为空
            raise TimeoutError
        return items.pop(0)
def put(x):
    with cond: items.append(x); cond.notify()
t0 = time.monotonic()
try: take(0.2)
except TimeoutError: print("timeout", time.monotonic() - t0 >= 0.2)   # True
threading.Timer(0.1, put, ["job"]).start()
print(take(1.0))                                                       # job
```

<details class="pt"><summary>延伸</summary>

测超时别真睡：把时钟注入进来，或者把超时设成几十毫秒。超时测试里断言“抛了 `TimeoutError`”，不要断言“恰好等了多久”。

</details>

**知识点：**条件变量（Condition Variables）
