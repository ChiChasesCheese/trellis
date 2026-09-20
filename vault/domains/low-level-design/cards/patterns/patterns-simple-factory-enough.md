---
id: patterns-simple-factory-enough
node: patterns.creational
type: qa
step: 2
---
## Q
为什么"根据一个字符串创建对象"这种 Simple Factory，在 Python 里往往直接是一个字典而不是一个专门的类？

## A
Python 的类本身就是一等对象，可以直接当成字典的值——查表调用比写一串 `if`/`elif` 或者专门声明一个工厂类更短，也更容易在运行时注册新类型。

```python
SHAPE_REGISTRY: dict[str, type] = {
    "circle": Circle,
    "square": Square,
}

def make_shape(kind: str, **kwargs) -> object:
    return SHAPE_REGISTRY[kind](**kwargs)
```

这样已经足够的场景：类型集合基本固定、各类型的构造签名一致。一旦调用方要自己注册新的构造逻辑（插件系统），或者不同类型需要完全不同的构造步骤，才值得升级到更结构化的形式。
