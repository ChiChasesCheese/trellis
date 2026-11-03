---
id: craft-init-subclass-registry-1-hand-written-registry
node: craft.idioms.init-subclass-registry
type: qa
step: 1
---
## Q
**__init_subclass__ 注册表 · 按名字创建实现，手写 dict 的两步代价**｜写法

缓存配置里写 `eviction: "lru"`，代码要据此创建对应的淘汰策略对象。最直接的写法是一个 `POLICIES = {"lru": LruPolicy, "lfu": LfuPolicy}` 字典加一个 `create(name)`。新增一种策略时要做哪两件事？漏了第二件会怎样？未知名字应该怎样报错？

## A
**要点。** 注册表（registry）是「名字 → 类」的映射，让配置里的字符串能变成对象，调用方不用 `import` 具体的类。手写字典的代价是新增一种实现要做两步：写类、去字典里登记；漏了第二步，类存在但配置里选不到，运行时才发现。未知名字时应抛带「已知名字清单」的配置错误，让用户一眼看出拼错了还是没登记。

```python
class ConfigError(ValueError): ...

class Policy: ...
class LruPolicy(Policy): ...
class LfuPolicy(Policy): ...

POLICIES: dict[str, type[Policy]] = {"lru": LruPolicy, "lfu": LfuPolicy}   # 手写登记

def create(name: str) -> Policy:
    if name not in POLICIES:
        raise ConfigError(f"unknown eviction policy {name!r}; known: {sorted(POLICIES)}")
    return POLICIES[name]()

class FifoPolicy(Policy): ...                    # 新增一种，忘了去登记

print(type(create("lru")).__name__)
try:
    create("fifo")
except ConfigError as e:
    print("ConfigError:", e)
```

实际输出：

```
LruPolicy
ConfigError: unknown eviction policy 'fifo'; known: ['lfu', 'lru']
```

**为什么。** 第二行就是漏登记的症状：`FifoPolicy` 已经定义了，却选不到；报错里列出的 `known` 让排查只需看一眼。显式字典有它的好处：用 grep 就能找到全部实现，导入顺序不影响结果，没有隐式的副作用。实现只有两三种，并且都在同一个文件里时，这就够了。

**信号。** 实现会由别的包提供（第三方插件），或者分散在许多模块里，手写字典就会变成一个人人都要改的集中点；这时才考虑让登记随类的定义自动发生。
