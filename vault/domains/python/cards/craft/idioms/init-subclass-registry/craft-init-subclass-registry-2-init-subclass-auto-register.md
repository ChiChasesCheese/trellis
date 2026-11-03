---
id: craft-init-subclass-registry-2-init-subclass-auto-register
node: craft.idioms.init-subclass-registry
type: qa
step: 2
---
## Q
**__init_subclass__ 注册表 · 让登记随类的定义自动发生**｜写法

想让「写一个策略类」就自动登记，不用再去改字典。`__init_subclass__` 是在子类定义时由 Python 调用的钩子，它怎样做到这一点？有哪些细节要写对？

## A
**要点。** 每当有类继承了基类，Python 就在子类创建完成后调用基类的 `__init_subclass__(cls, **kwargs)`。类定义时可以写 `class Lru(Policy, name="lru")`，关键字参数会传给这个钩子。钩子里把 `cls` 存进注册表即可：类一定义完就登记，不可能漏。要注意三点：调用 `super().__init_subclass__(**kwargs)` 保持链条完整；不带 `name` 的中间基类不登记；重名要报错，而不是悄悄覆盖。

```python
class ConfigError(ValueError): ...

class Policy:
    registry: dict[str, type["Policy"]] = {}
    def __init_subclass__(cls, /, name: str | None = None, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if name is not None:                     # 不带 name 的中间基类不登记
            if name in Policy.registry:
                raise ConfigError(f"duplicate policy name {name!r}")
            Policy.registry[name] = cls          # 类一定义完就登记

class LruPolicy(Policy, name="lru"): ...
class LfuPolicy(Policy, name="lfu"): ...
class FifoPolicy(Policy, name="fifo"): ...      # 新增一种：写类即登记

def create(name: str) -> Policy:
    if name not in Policy.registry:
        raise ConfigError(f"unknown policy {name!r}; known: {sorted(Policy.registry)}")
    return Policy.registry[name]()

print(sorted(Policy.registry))
print(type(create("fifo")).__name__)
try:
    class Dup(Policy, name="lru"): ...
except ConfigError as e:
    print("ConfigError:", e)
```

实际输出：

```
['fifo', 'lfu', 'lru']
FifoPolicy
ConfigError: duplicate policy name 'lru'
```

**为什么。** 新增 `FifoPolicy` 只写了一行类定义，`create("fifo")` 就能用，「写类 + 登记」两步合成了一步。重名检查是必要的：两个模块各自注册同一个名字，没有它，后导入的会悄悄顶掉先导入的，行为取决于导入顺序。

**对比。** 更重的做法是元类（metaclass）或类装饰器；`__init_subclass__` 是其中最轻的，能做到「类定义时做一件事」就不要用元类。
