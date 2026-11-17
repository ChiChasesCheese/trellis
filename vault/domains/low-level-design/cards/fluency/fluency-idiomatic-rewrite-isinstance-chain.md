---
id: fluency-idiomatic-rewrite-isinstance-chain
node: fluency.idiomatic-rewrite
type: qa
step: 2
---
## Q
折扣计算里有一串 `if isinstance(d, Percent): … elif isinstance(d, Flat): … else: raise`。怎么改成 `match`？改成 `functools.singledispatch` 或者把逻辑挪进类里，各自在什么情况下更合适？

## A
**同一处枚举所有类型用 `match`，要开放扩展用分派**

- **`match` 把“判断类型”和“取字段”合成一步**：`case Percent(pct)` 按位置取字段，dataclass 自动生成 `__match_args__`，需要 3.10 以上；
- **兜底分支要写**：`case _` 抛 `TypeError`，没有它，新增类型会悄悄返回 `None`；
- **`case Percent:` 不是类型判断**：不带括号的裸名字是捕获模式，匹配任何值并绑定到这个名字；类型判断要写 `case Percent():`；
- **`singledispatch` 适合开放集合**：别的模块可以给新类型 `register`，按第一个参数的类型（含父类）分派，调用方不用改；
- **自己拥有的类型，最好是多态方法**：`d.apply(price)`，新增类型不用动任何分支；`match` 是类型不归你管（数据类、解析结果）时的选择。

```python
from dataclasses import dataclass
@dataclass(frozen=True)
class Percent: pct: int
@dataclass(frozen=True)
class Flat: cents: int
def apply(d, price):
    match d:
        case Percent(pct): return price * (100 - pct) // 100
        case Flat(cents): return max(price - cents, 0)
        case _: raise TypeError(type(d))
print(apply(Percent(10), 200), apply(Flat(500), 200))   # 180 0
```

<details class="pt"><summary>延伸</summary>

`match` 还能解构嵌套结构和带条件的分支（`case Flat(c) if c > 1000`）。但如果同样的 `match` 在三处代码里重复出现，说明该用多态了。

</details>

**知识点：**改写成地道代码（Idiomatic Rewrite）
