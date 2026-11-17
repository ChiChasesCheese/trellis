---
id: concurrency-depth-per-call-state
node: concurrency-depth.confinement
type: qa
step: 6
---
## Q
一个 `Pipeline` 实例被多个线程复用，`run(items)` 把中间结果存在 `self._out`。两个线程同时调用 `run`，会得到什么？状态该放在哪？

## A
**每次调用的状态放局部变量，实例上只放不变的配置**

- **现象**：两次调用共用 `self._out`，后到的调用把它重置，之后两个调用往同一个列表里追加，各自拿到的是同一个混合列表。实测（两个线程各处理 2 个元素，20 轮）：每轮两个调用拿到的内容相同，且都有 4 个元素；
- **原因**：实例属性是共享的，局部变量在调用自己的栈帧里，天然线程封闭；
- **规则**：构造后不再改的东西（配置、策略、不可变表）放实例上，可以被所有线程共享；每次调用才有的东西（结果、窗口、临时表）放局部变量；
- **同样适用于**：模块级的全局缓存、可变默认参数 `def f(x, acc=[])`，它们都在调用之间共享；
- **好处**：实例无状态，就能被并发复用，也不需要锁，测试也简单。

```python
import time
from concurrent.futures import ThreadPoolExecutor
class Bad:
    def run(self, items):
        self._out = []                      # 实例属性：所有调用共用
        for x in items: time.sleep(0.01); self._out.append(x * 2)
        return self._out
class Good:
    def run(self, items):
        out = []                            # 局部变量：每次调用一份
        for x in items: time.sleep(0.01); out.append(x * 2)
        return out
for p in (Bad(), Good()):
    with ThreadPoolExecutor(2) as ex: a, b = ex.map(p.run, ([1, 2], [10, 20]))
    print(a is b)                           # Bad True / Good False
```

**知识点：**不靠锁的线程安全（Immutability & Confinement）
