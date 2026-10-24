---
id: pl-meta-dynamic-intro-metaclass
node: metaprogramming.dynamic-features
type: qa
step: 4
---
## Q
Python 的元类（metaclass）和 `__init_subclass__` 是什么？为什么「类也是对象」这件事让它们成为可能？

## A
**前提**：在 Python 里 `class Foo: ...` 是一条在运行时执行的语句，它创建一个类对象。类对象也有自己的类型，默认是 `type`。`type` 就是「创建类的类」，也叫元类。

**元类**：你可以指定一个自己的元类，`class Foo(metaclass=Meta)`。以后每次创建 `Foo` 或它的子类，Python 都会调用 `Meta` 的 `__new__`，给你一个机会在类诞生那一刻检查、修改、登记它。

```python
registry = {}
class Meta(type):
    def __new__(m, name, bases, ns):
        c = super().__new__(m, name, bases, ns); registry[name] = c; return c
class Plugin(metaclass=Meta): pass
class Foo(Plugin): pass
# list(registry) -> ['Plugin', 'Foo']
```

真实输出：`['Plugin', 'Foo']`。定义子类时没有任何注册语句，登记自动发生。

**`__init_subclass__`**：Python 3.6 引入的轻量替代。父类里写 `def __init_subclass__(cls, **kw)`，每次有子类定义，它被自动调用。90% 的「子类自动注册」「检查子类必须实现某方法」用它就够，不需要元类。

**心智模型**：元类是「类的工厂」，能改变类的一切；`__init_subclass__` 是「子类诞生时的回调」，范围小得多。

**要记住的一点**：Django 的 `models.Model`、SQLAlchemy 的声明式基类、Enum、ABC 都用了元类；多个元类会冲突，所以日常业务代码应尽量不用。
