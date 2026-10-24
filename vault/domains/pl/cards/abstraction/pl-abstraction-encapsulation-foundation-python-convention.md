---
id: pl-abstraction-encapsulation-foundation-python-convention
node: abstraction.encapsulation
type: qa
step: 5
---
## Q
Python 没有 `private` 关键字，单下划线、双下划线（名字改写）和 `property` 分别起什么作用？

## A
Python 的态度是「我们都是成年人」（consenting adults）：语言不阻止你访问任何东西，靠命名约定传达意图。

- **`_x`（单下划线）**：约定「内部使用，不属于公开 API」。语言不做任何限制，工具（IDE、`from m import *`）会尊重这个约定。
- **`__x`（双下划线）**：触发**名字改写**（name mangling）：类内的 `__x` 被改名为 `_类名__x`，目的是避免子类不小心重名，**不是**安全机制。

```python
class Account:
    def __init__(self): self.__balance = 100
a = Account()
a.__balance          # AttributeError: no attribute '__balance'
a._Account__balance  # 100：改名后的字段照样能读
```

- **`property`**：把方法伪装成属性，让你能在不改调用方的情况下加校验：

```python
@property
def c(self): return self._c
@c.setter
def c(self, v):
    if v < -273.15: raise ValueError("below absolute zero")
    self._c = v
t.c = -300     # ValueError: below absolute zero
t._c = -999    # 没有任何东西阻止这行
```

`property` 守住的是**公开入口**的不变量，不是防备恶意代码。这是 Python 封装的全部含义：一套让同事知道哪些东西能碰的礼貌，而不是一堵墙。
