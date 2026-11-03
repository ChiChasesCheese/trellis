---
id: craft-init-subclass-registry-4-explicit-decorator-and-test-isolation
node: craft.idioms.init-subclass-registry
type: qa
step: 4
---
## Q
**__init_subclass__ 注册表 · 全局注册表、装饰器登记与测试隔离怎么取舍**｜写法

自动登记把类塞进一个全局字典。测试里临时定义了一个假的策略类，就永久留在注册表里，影响其他测试。换成显式装饰器登记、并且每个工厂有自己的登记表，取舍是什么？

## A
**要点。** 三种登记方式的取舍：手写字典最直白，改动集中；`__init_subclass__` 最省事，但隐式、依赖导入、登记表是全局可变状态；装饰器登记居中，登记写在类旁边（grep 得到、不依赖继承关系），并且登记表可以是工厂对象自己的，测试里造一个新工厂就是干净的环境。

```python
from collections.abc import Callable

class ConfigError(ValueError): ...

class Factory:
    """每个工厂自带一份登记表，而不是全局的。"""
    def __init__(self) -> None:
        self._makers: dict[str, Callable[[], object]] = {}
    def register(self, name: str):
        def deco(cls):
            if name in self._makers:
                raise ConfigError(f"duplicate name {name!r}")
            self._makers[name] = cls
            return cls                           # 装饰器原样返回类，不改它
        return deco
    def create(self, name: str) -> object:
        try:
            return self._makers[name]()
        except KeyError:
            raise ConfigError(f"unknown {name!r}; known: {sorted(self._makers)}") from None

policies = Factory()

@policies.register("lru")                        # 登记写在类旁边，grep "register(" 就能找到全部
class LruPolicy: ...

@policies.register("lfu")
class LfuPolicy: ...

print(type(policies.create("lru")).__name__)

def test_with_fake_policy() -> None:
    local = Factory()                             # 测试里造一个干净的，不污染全局
    @local.register("fake")
    class Fake: ...
    assert type(local.create("fake")).__name__ == "Fake"
test_with_fake_policy()
print(sorted(policies._makers))                  # 全局的没被测试弄脏
```

实际输出：

```
LruPolicy
['lfu', 'lru']
```

**为什么。** 最后一行显示测试里注册的 `fake` 没有进入全局登记表，因为它登记在测试自己新建的 `Factory` 上。若用全局的 `__init_subclass__` 注册表，测试定义的 `Fake` 类会一直留下，测试顺序一变就可能出现重名或残留。装饰器原样返回类，不改变类本身。

**判据。** 实现少、都在一两个模块里：手写字典。需要第三方插件扩展，或实现分散在许多模块：自动或装饰器登记，并保证登记表可被替换；要继承关系自然成立（所有策略都是 `Policy` 的子类）并且名字取自类定义，`__init_subclass__` 最自然。
