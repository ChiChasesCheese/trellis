---
id: pl-eng-apidesign-pitfall-mutable-default
node: engineering.api-design
type: qa
step: 11
---
## Q
Python 函数的可变默认参数（比如 `bucket=[]`）为什么会在多次调用间共享状态？API 里应该怎样表示“默认是空列表”？

## A
Python 的默认值在 **`def` 语句执行时求值一次**，之后每次调用没有传该参数时，用的都是同一个对象。默认值如果是列表、字典、集合这样的可变对象，所有调用共享它：
```python
def add(item, bucket=[]):
    bucket.append(item)
    return bucket
print(add(1), add(2))      # [1, 2] [1, 2]
```
第二次调用并没有拿到一个新的空列表，`bucket` 还是第一次那个，里面已经有 `1`。两次打印出的是同一个列表对象，所以看到的都是 `[1, 2]`。这类 bug 常常跨请求泄漏数据，在多线程下还会变成数据竞争。

**为什么这样设计**：默认值表达式只求值一次，函数定义本身也就是一个运行时语句。好处是性能与简单（默认值就存在函数对象上，可以通过 `add.__defaults__` 看到）；坏处是它与直觉不符。

**正确的 API**：用 `None` 做“没传”的哨兵，在函数体里创建新对象：
```python
def add(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```
**其他语言没有这个问题**：Java 和 Go 根本没有默认参数，Rust 的 `Default` 在调用时构造新值。

**延伸**：这条规则也适用于 `dataclass` 字段：`@dataclass class C: items: list = []` 会直接报错（`ValueError: mutable default ... use default_factory`），要写 `field(default_factory=list)`。静态检查工具（`ruff` 的 `B006`、`pylint`）会检查这类问题，团队应该在 CI 里打开。
