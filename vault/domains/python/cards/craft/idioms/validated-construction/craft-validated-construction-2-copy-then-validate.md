---
id: craft-validated-construction-2-copy-then-validate
node: craft.idioms.validated-construction
type: qa
step: 2
---
## Q
**构造即校验 · 先拷贝再校验，`object.__setattr__` 为什么安全**｜写法

计费方案 `PayPlan` 收一个费率字典，在 `__post_init__` 里校验「每个状态都有非负费率」。校验通过了，调用方之后改了自己手里的字典，对象会怎样？为什么要先把字典拷成只读视图、再校验？

## A
**要点。** 校验检查的是**这一刻**对象指向的数据。如果字段和调用方共享同一个可变容器（别名，alias），校验通过后调用方一改，对象就悄悄变成非法的。做法是两步：先拷贝成只读副本，再校验**副本**。冻结类里给字段赋值只能走 `object.__setattr__`，它绕过冻结机制，只在构造期间安全：此时对象还没交给任何人，没有别的引用能观察到半成品。

```python
@dataclass(frozen=True)
class AliasPlan:
    rates: Mapping[str, int]
    def __post_init__(self) -> None:
        if any(r < 0 for r in self.rates.values()):     # 校验了调用方的字典
            raise ValueError("negative rate")

@dataclass(frozen=True)
class CopyPlan:
    rates: Mapping[str, int]
    def __post_init__(self) -> None:
        # 先拷贝成只读视图，再校验这份拷贝；frozen 下只能绕过 __setattr__
        object.__setattr__(self, "rates", MappingProxyType(dict(self.rates)))
        if any(r < 0 for r in self.rates.values()):
            raise ValueError("negative rate")

mine = {"driving": 5}
a, c = AliasPlan(mine), CopyPlan(mine)
mine["driving"] = -100                  # 构造之后，调用方改了自己手里的字典
print("别名版 看到:", dict(a.rates), "<- 已经通过校验的对象变成了非法")
print("拷贝版 看到:", dict(c.rates))
try:
    c.rates["driving"] = 0               # 想通过对象改也不行
except TypeError as e:
    print("只读视图:", e)
try:
    c.rates = {}                         # 重新绑定字段被 frozen 拦下
except Exception as e:
    print("frozen:", type(e).__name__)
```

实际输出：

```
别名版 看到: {'driving': -100} <- 已经通过校验的对象变成了非法
拷贝版 看到: {'driving': 5}
只读视图: 'mappingproxy' object does not support item assignment
frozen: FrozenInstanceError
```

**为什么。** 两个问题一次解决：`dict(...)` 切断别名，`MappingProxyType` 让别人通过这个对象也改不了。只做其中之一都不够：只拷贝不包装，字段能被对象的使用者改；只包装不拷贝，底层仍是调用方的字典，视图会跟着变。

**易错。** `MappingProxyType` 只保护第一层，值如果是 list 或 dict 依旧可变；值要用 tuple / frozenset / 数值。顺序也重要：先赋值规范化后的字段，再校验它。
