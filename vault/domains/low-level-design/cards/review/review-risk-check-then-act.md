---
id: review-risk-check-then-act
node: review.risk-patterns
type: qa
step: 2
---
## Q
评审时看到 `if stock > 0:` 后面跟着 `stock -= 1`，单线程测试都通过。为什么这在并发下是个典型的缺陷？怎么改？

## A
**“先检查、再动作”是两步：中间别的线程可以插进来**

- **检查和动作之间有窗口**：两个线程都看到库存为 1，都通过检查，都扣一次，结果卖出两件，库存变成 -1；
- **GIL 不能救你**：它只保证单条字节码是原子的，不保证“比较再减一”这两步连在一起；
- **修法一**：用同一把锁把检查和动作放进同一个临界区（`with lock:`）；
- **修法二**：让存储层做原子操作，比如数据库里 `UPDATE ... SET n = n - 1 WHERE n > 0`，看影响了几行；
- **评审信号**：对共享的字典、计数器、文件，出现 `if x not in d: d[x] = ...`、`if exists: ... else: create` 这类形状。

```python
import threading, time, contextlib

def run(lock):
    stock, sold = {"n": 1}, []
    def buy(u):
        with lock:
            if stock["n"] > 0:                 # 检查
                time.sleep(0.01)               # 放大窗口，让交错必现
                stock["n"] -= 1; sold.append(u)    # 动作
    ts = [threading.Thread(target=buy, args=(u,)) for u in "xy"]
    [t.start() for t in ts]; [t.join() for t in ts]
    return len(sold)

print(run(contextlib.nullcontext()), run(threading.Lock()))   # 2 1：没锁卖出两件
```

**知识点：**diff 里的高风险信号（Risk Patterns）
