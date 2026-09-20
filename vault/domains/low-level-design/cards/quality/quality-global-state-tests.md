---
id: quality-global-state-tests
node: quality.testability
type: qa
step: 4
---
## Q
模块级的全局状态是怎么破坏测试的？以时间依赖为例，标准修法是什么？

## A
两种破坏方式：一是没有可替换的位置——一个函数内部直接调用 `datetime.now()` 或读一个模块级变量，测试没有任何参数能把这个依赖换掉，只能被迫拖着真实实现一起跑；二是状态在测试之间泄漏——一个可变的模块级变量跨测试用例存活，于是单独跑这个测试能过、整个套件一起跑（或者并行跑）就可能挂,取决于执行顺序,这是最难排查的一类不稳定测试（flaky test）。

```python
class Clock(Protocol):
    def now(self) -> datetime: ...

class FixedClock:
    def __init__(self, value: datetime):
        self._value = value
    def now(self) -> datetime:
        return self._value
```
领域逻辑永远不直接调用 `datetime.now()`，而是接受一个注入的 `Clock`；测试传 `FixedClock(...)`，既能断言确定的时间点，也能显式"推进"时间来测试超时之类的逻辑。同样的配方适用于随机性（注入一个 `Random` 实例或种子）和 id 生成（注入一个 `IdGenerator`）。
