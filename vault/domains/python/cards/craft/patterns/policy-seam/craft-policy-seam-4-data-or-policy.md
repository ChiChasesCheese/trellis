---
id: craft-policy-seam-4-data-or-policy
node: craft.patterns.policy-seam
type: qa
step: 4
---
## Q
**策略接缝 · 什么时候别抽策略：换城市的价目表是数据，不是算法**｜写法

网约车计价有两类会变的东西：每个城市的价目表（起步价、每公里、每分钟），和动态加价（按等车人数 ÷ 可派车数分档）。是不是都要抽成策略接口？

## A
**要点。** 判据：变的是**数值**还是**逻辑**。价目表只是三个数，换城市就是换一张表，写成 `frozen dataclass` 的数据，任何人都不需要继承什么。加价档位是「按比值查表」的逻辑，而且业务上真的会换成别的算法（比如按天气加价），所以才是一个可替换的函数，默认值是不加价。

```python
@dataclass(frozen=True, slots=True)
class FareTable:
    """它是数据不是算法，所以是 frozen dataclass 而不是抽象基类。"""
    base: int
    per_km: int
    per_minute: int

SurgePolicy = Callable[[RideRequest, int, int], Fraction]   # (请求, 等车数, 可派数) -> 倍数

def no_surge(request, waiting, available) -> Fraction:
    return Fraction(1)                                       # 下界，也是测试最省心的基线
```

**为什么。** 抽象的成本是读代码的人多跳一层，收益是以后换实现时不改核心。只有一种实现、也想不出第二种的地方，这个收益是零，成本却是真的。反过来，真会变的逻辑如果写死，每次业务调整都要改计价的核心。

**判据三问。** ①这条规则会不会换？（只是配置值变化 → 数据）②换的时候我是否希望不碰库存和状态机？（是 → 接缝）③我能说出第二个有意义的实现吗？（说不出 → 先别抽）。

**易错。** 先抽接口再找实现，常导致接口形状只适合第一个实现；等第二个实现出现时再抽，接口才长得对。

**对照。** 倍数用 `Fraction` 而不是 `float`：它乘进金额，二进制浮点的 1.2 不是 1.2，几千万单之后对不上的那几分钱没人说得清。
