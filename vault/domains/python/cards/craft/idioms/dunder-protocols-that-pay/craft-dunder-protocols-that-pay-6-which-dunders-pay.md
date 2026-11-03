---
id: craft-dunder-protocols-that-pay-6-which-dunders-pay
node: craft.idioms.dunder-protocols-that-pay
type: qa
step: 6
---
## Q
**特殊方法 · 什么时候值得写，什么时候不该写**｜写法

限流结果的 `__bool__`、过滤器的 `&`、流水线的 `+`、线程池的 `with`，这些特殊方法分别在什么情形下让代码变得更好？哪些特殊方法即使写了看起来很漂亮，也应该拒绝？

## A
**要点。** 判据只有一条：写了之后，调用点是否更自然，或者以后改实现时调用点是否不用动。如果调用点读起来更像是在用内置类型，或者类型升级后旧代码照常工作，就值得；如果写的方法会改变语言的基本语义，或者让读代码的人猜，就不该。

```python
# rate-limiter：结果从 bool 升级成 Decision，旧调用点 `if limiter.allow(k):` 不动
def __bool__(self) -> bool:
    return self.allowed

# amz-linux-find：过滤器组合返回新对象，读起来像查询
def __and__(self, other: "Filter") -> "Filter":
    return AndFilter(self, other)

# image-transform-pipeline：流水线相加 = 步骤拼接，仍是不可变的新流水线
def __add__(self, other: Pipeline) -> Pipeline:
    return Pipeline(self.steps + other.steps)

# thread-pool：with 块保证退出时关闭，不会忘了 join
def __enter__(self) -> ThreadPool:
    return self
def __exit__(self, *exc_info: object) -> None:
    self.shutdown(wait=True)
```

不变的是：方法体都很短，委托给已有的普通方法，结果类型与操作数同类。变的是解决的问题：兼容升级（`__bool__`）、代数组合（`& | ~ +`）、资源生命周期（`with`）。

**不该写。** `__eq__` 和 `__hash__` 会改变相等与字典键的含义，写错就让对象在集合里表现怪异；`__getattr__` 会把拼写错误变成静默的 `None` 或无限递归；`__getitem__` 用来做与下标无关的查询，读者猜不到。需要这些行为时，用冻结数据类自动生成 `__eq__`/`__hash__`，用普通命名方法做查询。

**见于。** rate-limiter、amz-linux-find、image-transform-pipeline、amz-in-memory-db（谓词对象可调用，返回三值逻辑）、splitwise（通知器可直接作观察者）、thread-pool、ttl-cache（语义对齐 dict）。

**信号。** 新类型很像一个内置类型（容器、数字、函数、上下文）；或者你正在把返回值从简单类型升级为对象，而不想改所有调用点。
