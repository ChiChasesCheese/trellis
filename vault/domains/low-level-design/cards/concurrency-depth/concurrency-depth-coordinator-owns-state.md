---
id: concurrency-depth-coordinator-owns-state
node: concurrency-depth.confinement
type: qa
step: 2
---
## Q
线程池并行处理一批文件，最后要汇总计数。让每个工作线程直接往共享的 `Counter` 里累加，还是让它们返回结果、由主线程汇总？后者为什么不用锁？

## A
**工作线程只返回值，可变状态只有协调线程碰**

- **线程封闭（thread confinement）**：每个可变对象规定只有一个线程能改它，别的线程碰不到，竞态就无从发生，不需要锁；
- **做法**：工作函数是纯函数，只读入参、返回新值；协调线程在 `for part in ex.map(...)` 里把结果并进汇总对象；
- **`ex.map` 按提交顺序给结果**，工作线程里抛的异常在迭代到那一项时重新抛出，协调线程统一处理；
- **代价**：每个工作线程的局部结果要在内存里留到汇总，合并是串行的；合并比计算还重的话，改成分层合并（树形归约）；
- **做不到的时候**：工作线程必须共享一个缓存或计数器，就回到加锁，或者让一个线程独占状态、别人发消息给它。

```python
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

def count_words(chunk: str) -> Counter:    # 纯函数：只返回值，不碰共享状态
    return Counter(chunk.split())

chunks = ["a b a", "b c", "a c c"]
total = Counter()
with ThreadPoolExecutor(4) as ex:
    for part in ex.map(count_words, chunks):
        total += part                      # 只有这个线程改 total
print(sorted(total.items()))               # [('a', 3), ('b', 2), ('c', 3)]
```

**知识点：**不靠锁的线程安全（Immutability & Confinement）
