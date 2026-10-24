---
id: pl-memory-reference-counting-foundation-cpython
node: memory.reference-counting
type: qa
step: 2
---
## Q
CPython 的引用计数怎么工作？循环垃圾检测器（cycle collector）补的是哪个洞？

## A
CPython 是 Python 最常用的官方实现。其中每个对象头部有一个计数字段，记录“有多少个引用指向我”：名字绑定、放进列表、作为参数传入都会加 1；名字重新绑定、`del`、容器销毁都会减 1。**减到 0 的瞬间对象立刻被销毁**，销毁时再给它引用的对象各减 1，可能连锁释放。

```python
a = Node()
print(sys.getrefcount(a))   # 2: the name `a` plus the call argument itself
b = a                       # count goes up
del b, a                    # count hits 0 -> freed immediately
```

洞在循环引用：`x.o = y; y.o = x` 之后即使删掉外部名字 `x`、`y`，两者各还剩 1 个来自对方的引用，计数永远不到 0，泄漏。为此 CPython 另带一个**循环垃圾检测器**，周期性地只检查容器类对象（列表、字典、实例）：先把每个容器的计数减去“来自其他容器内部的引用”，剩下计数仍大于 0 的说明有外部引用（栈、全局），是活的；从它们出发能到达的也是活的；其余就是孤立的环，统一销毁。可以用 `gc.collect()` 手动触发。

要记住的一个事实：CPython 对大多数对象即时回收（所以文件对象用完常常立刻关闭），但这是实现细节，不是语言承诺；环要等检测器扫描才回收。
