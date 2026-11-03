---
id: craft-protocol-callable-abc-3-template-method
node: craft.idioms.protocol-callable-abc
type: qa
step: 3
---
## Q
**策略接口 · 共享算法骨架时用 ABC，子类漏写方法何时报错**｜写法

限流器有固定窗口、滑动窗口、令牌桶等四种算法，判定流程（`check` 先判定、`try_acquire` 判定后扣额度）完全相同，只有「当前占用多少」「还要等多久」「怎么扣」不同。接口怎么选？有人漏写了其中一个方法，错误在什么时候暴露？

## A
**要点。** 共享的是**流程**，不是签名：基类用具体方法写好骨架，把变化的步骤留成抽象方法，这就是模板方法（template method）。此时必须是 ABC 而不是 Protocol，因为 Protocol 不能把骨架交给实现者。`@abstractmethod` 有个好处：子类漏写，**实例化时**就抛 `TypeError`，不用等到某次调用才炸。

```python
from abc import ABC, abstractmethod

class Handler(ABC):
    def handle(self, msg: str) -> str:          # 具体方法：骨架只写一次
        return self.emit(msg.strip().upper())

    @abstractmethod
    def emit(self, text: str) -> str: ...      # 子类必须给出

class Console(Handler):
    def emit(self, text): return f"[console] {text}"

class Forgot(Handler):
    pass                                       # 忘了实现 emit

print(Console().handle(" hi "))
try:
    Forgot()                                   # 报错发生在实例化，不是第一次调用
except TypeError as e:
    print("实例化时报错:", e)

# 对照：没有 abstractmethod，忘了实现要等到真正调用才暴露
class Lazy:
    def handle(self, msg): return self.emit(msg)
x = Lazy()
print("构造成功，调用才炸:", end=" ")
try:
    x.handle("hi")
except AttributeError as e:
    print(e)
```

实际输出（Python 3.12 起的措辞；3.11 写成 `Can't instantiate abstract class Forgot with abstract method emit`）：

```
[console] HI
实例化时报错: Can't instantiate abstract class Forgot without an implementation for abstract method 'emit'
构造成功，调用才炸: 'Lazy' object has no attribute 'emit'
```

**为什么。** 限流器基类把「额度不够时被拒绝，一份额度都不扣」写在 `try_acquire` 里一次，四个子类不会各自写错一遍。不用 ABC 的话，这段流程会被复制四份，而且四份会慢慢走样。

**易错。** 骨架里的变化点要尽量少且小。抽象方法超过四五个，或者子类需要覆盖具体方法，说明基类做太多事，考虑改成组合：把变化的部分作为参数传进来。
