---
id: pl-binding-evaluation-strategy-mechanism
node: binding.evaluation-strategy
type: qa
step: 6
---
## Q
传名（call by name）和按需求值（call by need）在实现上差在哪里？用一个能数出调用次数的例子说明 thunk 的缓存。

## A
两者都把参数包装成**无参数的函数**（thunk），不同之处只有一点：算完之后**记不记住结果**。

- 传名：每次用到参数就调用一次这个函数。
- 按需求值：第一次调用时算出结果存起来，之后直接读存起来的值。

在严格求值的语言里可以手工实现。下面用 Python 的闭包模拟，数一数昂贵函数被调用了几次：

```python
class Lazy:                          # call by need: a thunk that caches
    def __init__(self, f): self.f, self.done = f, False
    def get(self):
        if not self.done: self.v, self.done = self.f(), True
        return self.v

calls = 0
def costly():
    global calls; calls += 1; return 42
```

先按需求值：创建 thunk 后连续取三次，再改成传名，每次都重新调用：

```python
t = Lazy(costly); t.get(); t.get(); t.get()
print("need:", calls)                # need: 1
calls = 0
name = lambda: costly()              # call by name: no cache
name(); name(); name()
print("name:", calls)                # name: 3
```

输出 `need: 1` 和 `name: 3`。

thunk 的成本也由此可见：

1. **每个 thunk 是一个堆对象**，保存闭包、状态位和结果槽。严格语言里一个整数参数只是寄存器里的一个字，惰性语言里则是一个对象，所以惰性语言编译器（GHC）要做**严格性分析**（strictness analysis）：证明某个参数反正一定会被用到，就把 thunk 优化回普通的求值。
2. **缓存带来空间问题**：thunk 求值前持有它的闭包和所有被捕获的变量，求值后才释放，这让内存占用难以预测。
3. **并发需要同步**：多个线程同时求值同一个 thunk，要么加锁，要么容忍重复计算。

在 Java、Python 等语言里手工写的 `Supplier`、`lambda` 就是传名，如果需要缓存要自己写（Guava 的 `Suppliers.memoize`，Python 的 `functools.cached_property` 和 `functools.cache`）。

结论：惰性不是魔法，是「闭包 + 一次性缓存」。理解这一点就能判断它什么时候值得付出堆分配和不可预测的时机。
