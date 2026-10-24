---
id: pl-eng-apidesign-found-python-kwargs
node: engineering.api-design
type: qa
step: 5
---
## Q
Python 的关键字参数、默认值和仅限关键字参数（keyword-only，参数列表里的 `*`）怎样让 API 保持可读和可演进？

## A
在 Go、Java、Rust、C++ 和 Python 里，只有 Python 把“可选参数”完整做进了语法：函数参数可以有默认值，调用时可以按名字传（C++ 有默认实参，却只能按位置传）。这让大多数 Java/Go 里需要构建器或选项的场景，在 Python 里就是一个函数签名。

问题是**位置参数**。`connect("db", 2, 0, False)` 读者无法知道 `2`、`0`、`False` 各是什么，而且一旦库作者调整参数顺序，旧调用者会悄悄地传错值。解法是**仅限关键字参数**：在参数列表里用 `*` 分隔，后面的参数必须按名字传。
```python
def connect(host, *, timeout=30, retries=3, tls=True): ...
connect("db", timeout=2)          # ('db', 2, 3, True)
connect("db", 2, 0, False)        # TypeError: connect() takes 1 positional argument but 4 were given
```
这个设计同时给了你三个好处：
1. 调用处自带名字，可读；
2. 库作者可以增加、调整可选参数的顺序，不会破坏旧代码；
3. 必填的主要参数仍然是位置参数，不啰嗦。

对应地，`/` 把前面的参数限定为仅限位置（`def f(a, b, /, c)`），让库作者保留以后改参数名的自由。

**鸭子类型**（duck typing）是 Python API 的另一个特点：函数只要求参数“有某些方法”，而不要求某个类。需要明确契约时，用 `typing.Protocol` 声明结构（类似 Go 的接口）：调用者不用继承，类型检查器（mypy、pyright）仍能验证。

**默认值的求值时机**是 Python 特有的陷阱：默认值在**函数定义时**求值一次，而不是每次调用。对列表、字典这类可变对象，这会让多次调用共享同一个对象。

做法：布尔标志和超过两个的可选参数一律设为仅限关键字；用 `None` 做哨兵表示“没传”。
