---
id: concurrency-depth-read-modify-write
node: concurrency-depth.compound-actions
type: qa
step: 2
---
## Q
`q = self.qty; self._audit(q); self.qty = q - 1` 这种“读、算、写”在 3.11 上默认间隔下跑几百轮都不丢更新，是不是说明它安全？锁怎么加？

## A
**读改写必须整段在锁里；测不出不等于安全**

- **丢更新（lost update）**：两个线程都读到 100，各自写回 99，两次扣减只算一次；
- **实测（3.11，4 线程各扣 5000 次，100 轮）**：中间带一次 Python 方法调用时，默认间隔 0/100 轮丢，1e-6 下 100/100 轮丢；
- **缺口里没有 Python 调用就测不出**：`d["n"] += 1`、`v = d["n"]; d["n"] = v + 1`，以及缺口里只放一个 `len("")` 这样的 C 函数调用，在 3.11 上两种间隔都是 0/100。3.11 主要在 Python 函数入口和循环回跳处响应切换请求，这类缺口里没有切换点；这是 CPython 实现细节，换版本会变，不能靠它；
- **3.14t**：同样的 `+=` 在默认间隔下 100/100 轮丢，因为没有 GIL，字节码之间随时可以并行；
- **修法**：判断和修改放进同一个 `with lock`；能不共享就不共享（每个线程算自己的，最后合并）。

```python
import threading

class Stock:
    def __init__(self, qty):
        self.qty, self._lock = qty, threading.Lock()
    def take(self, n):
        with self._lock:                 # 读、判断、写是一个整体
            if self.qty < n:
                raise ValueError("insufficient")
            self.qty -= n
            return self.qty

s = Stock(5)
print(s.take(2), s.take(3))              # 3 0
```

<details class="pt"><summary>延伸</summary>

代码评审里看到“共享变量先读后写、中间有任何调用”，直接按有竞态处理；不要等测试红了才信。

</details>

**知识点：**复合操作（Compound Actions）
