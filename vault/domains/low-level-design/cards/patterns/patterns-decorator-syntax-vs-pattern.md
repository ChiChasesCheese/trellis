---
id: patterns-decorator-syntax-vs-pattern
node: patterns.structural
type: qa
step: 6
---
## Q
`@decorator` 这个语法糖和 Decorator 设计模式是什么关系？两者可以互相替代吗？

## A
`@decorator` 只是"在定义时用一个函数包一个函数或类"的语法糖——`@staticmethod`、`@dataclass` 都用这个语法，却完全不是 Decorator 模式（它们不是在运行时给对象叠加行为，而且经常改变了被包装对象的性质）。Decorator 模式说的是"在运行时用同一个接口层层包装对象，每层加一点行为"，用类来实现完全不需要 `@` 语法。反过来，`@decorator` 语法确实可以用来实现这个模式，比如给函数叠加日志、计时、缓存这些不改变函数签名的包装：

```python
def with_logging(fn):
    def wrapper(*args, **kwargs):
        print(f"call {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

@with_logging
def process(order_id: int) -> None: ...
```
