---
id: craft-replace-for-state-change-3-post-init-reruns
node: craft.idioms.replace-for-state-change
type: qa
step: 3
---
## Q
**用 replace 表达状态变化 · `replace` 会重新运行 `__post_init__`，这对带校验的类意味着什么**｜写法

方案类的 `__post_init__` 里有校验（cap 不能小于最大费率）和规范化（费率排序）。对它调用 `replace(plan, cap=2)` 会绕过校验吗？有派生字段（`init=False`）的类能用 `replace` 吗？

## A
**要点。** `dataclasses.replace` 不是复制后改字段，而是用旧对象的字段加上你给的新值，**重新调用构造函数**，所以 `__post_init__` 会再运行一次：校验照常拦截非法的新状态，规范化再做一遍。这是好事：不会因为走 `replace` 就绕过不变量。代价是规范化必须**幂等**（对已规范化的值再做一次结果不变），否则每次替换都会漂移。`init=False` 的字段不能传给 `replace`，会抛错（3.12 及以前是 `ValueError`，3.14 起是 `TypeError`），它们由 `__post_init__` 重新派生。

```python
from dataclasses import dataclass, field, replace

@dataclass(frozen=True)
class Plan:
    rates: tuple[int, ...]
    cap: int

    def __post_init__(self) -> None:
        print("  __post_init__ 运行")
        if self.cap < max(self.rates):
            raise ValueError("cap 小于某个费率")
        object.__setattr__(self, "rates", tuple(sorted(self.rates)))   # 规范化

@dataclass(frozen=True)
class WithDerived:
    base: int
    double: int = field(init=False)             # 派生字段, 不在 __init__ 里

    def __post_init__(self) -> None:
        object.__setattr__(self, "double", self.base * 2)

p = Plan((3, 1, 2), 10)
print("replace 改 cap=2 (小于最大费率 3):")
try:
    replace(p, cap=2)
except (ValueError, TypeError) as e:   # 3.12 及以前 ValueError，3.14 起 TypeError
    print("  拒绝:", e)
print("replace 改 cap=20:")
q = replace(p, cap=20)
print("  规范化是幂等的:", q.rates)

w = WithDerived(5)
try:
    replace(w, double=1)
except (ValueError, TypeError) as e:   # 3.12 及以前 ValueError，3.14 起 TypeError
    print("init=False 字段不能被 replace:", e)
print("改 base 会重新派生:", replace(w, base=7).double)
```

实际输出：

```
  __post_init__ 运行
replace 改 cap=2 (小于最大费率 3):
  __post_init__ 运行
  拒绝: cap 小于某个费率
replace 改 cap=20:
  __post_init__ 运行
  规范化是幂等的: (1, 2, 3)
init=False 字段不能被 replace: field double is declared with init=False, it cannot be specified with replace()
改 base 会重新派生: 14
```

**为什么。** 与「构造即校验」配合：构造函数是不变量的唯一守门人，`replace` 也必须走它。若手动 `object.__setattr__` 绕过构造改字段，就丢了这道保护。

**易错。** `__post_init__` 里如果有副作用（打日志、登记注册表），每次 `replace` 都会再触发一次。副作用不要放进 `__post_init__`。
