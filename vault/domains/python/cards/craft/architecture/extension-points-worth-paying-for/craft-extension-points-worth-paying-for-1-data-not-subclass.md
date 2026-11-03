---
id: craft-extension-points-worth-paying-for-1-data-not-subclass
node: craft.architecture.extension-points-worth-paying-for
type: qa
step: 1
---
## Q
**值得付费的扩展点 · 披萨店新增一种配料，要改多少代码**｜架构

点餐系统有尺寸、饼底、配料；配料有按尺寸不同的价格，有的配料之间互斥（蘑菇和菠萝不能同吃）。常见写法是每种配料一个子类，各自实现 `price()`。每上一种新配料要动哪里？有没有更便宜的扩展方式？

## A
**要点。** 变化的维度如果只是「有几种、各自多少钱、跟谁冲突」，就写成数据而不是代码。菜单是一个冻结的数据结构，价格计算和冲突检查是读这份数据的通用代码，新增配料只加一行数据，计算与校验的代码一行不动。为「将来会加配料」付的费用是：把配料描述成 `ToppingSpec` 这种结构，而不是散落在类里的方法。

```python
@dataclass(frozen=True)
class ToppingSpec:
    prices: dict[str, int]                         # 尺寸 -> 价格（分）
    excludes: frozenset[str] = frozenset()         # 互斥的配料

@dataclass(frozen=True)
class Menu:
    base: dict[str, int]
    toppings: dict[str, ToppingSpec]
    def price(self, size: str, toppings: list[str]) -> int:
        return self.base[size] + sum(self.toppings[t].prices[size] for t in toppings)
    def check(self, toppings: list[str]) -> None:
        for t in toppings:
            clash = self.toppings[t].excludes & set(toppings)
            if clash:
                raise ValueError(f"{t} 与 {sorted(clash)} 互斥")

menu = Menu({"M": 1000, "L": 1200},
            {"cheese": ToppingSpec({"M": 100, "L": 150})})
print("加奶酪 M:", menu.price("M", ["cheese"]))

# 新增配料：只加一行数据，price/check 一行不动
menu.toppings["mushroom"] = ToppingSpec({"M": 120, "L": 180}, excludes=frozenset({"pineapple"}))
menu.toppings["pineapple"] = ToppingSpec({"M": 130, "L": 190}, excludes=frozenset({"mushroom"}))
print("奶酪+蘑菇 L:", menu.price("L", ["cheese", "mushroom"]))
try:
    menu.check(["mushroom", "pineapple"])
except ValueError as e:
    print("互斥规则也是数据:", e)
```

菜单初始只有奶酪（M 号 100、L 号 150，基础价 M 1000、L 1200）；加入蘑菇和菠萝后计价、检查互斥，实际输出：

```
加奶酪 M: 1100
奶酪+蘑菇 L: 1530
互斥规则也是数据: mushroom 与 ['pineapple'] 互斥
```

**为什么。** 子类方案每加一种配料都是新增类、改工厂、改测试；数据方案还能从配置文件加载，让不写代码的人也能改菜单。

**代价。** 数据驱动有边界：规则一旦复杂到需要条件分支和组合（买二送一、套餐折扣），数据结构会越长越像一门语言，这时候再回到代码（策略函数）更清楚。
