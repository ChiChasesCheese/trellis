---
id: craft-money-types-3-money-value-object
node: craft.idioms.money-types
type: qa
step: 3
---
## Q
**金额类型 · `Money` 值对象为什么在币种不同时直接抛错**｜写法

云计费的 `Money` 是「整数分 + 币种」的冻结对象。`Money(100, "USD") + Money(100, "EUR")` 应该返回什么？为什么不是返回其中一个币种，或者一个自动换算后的结果？

## A
**要点。** 抛错。跨币种相加没有正确答案：悄悄返回其中一个币种会凭空造出或抹掉钱；自动换算需要汇率，而汇率有时间、有来源，不是加法该知道的事。让运算在类型层面拒绝，bug 在第一次相加时就暴露，而不是月底对账才发现。

```python
class BillingError(Exception): ...

@dataclass(frozen=True)
class Money:
    cents: int
    currency: str = "USD"

    @staticmethod
    def from_decimal(amount: Decimal, currency: str = "USD") -> "Money":
        return Money(int((amount * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP)), currency)

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise BillingError(f"币种不同：{self.currency} 与 {other.currency}")   # 绝不猜
        return Money(self.cents + other.cents, self.currency)

@dataclass(frozen=True, order=True)
class SortableMoney:
    cents: int
    currency: str = "USD"

print(Money(150) + Money.from_decimal(Decimal("2.505")))   # 2.505 元 -> 251 分
try:
    Money(100, "USD") + Money(100, "EUR")
except BillingError as e:
    print("跨币种相加:", e)
print("order=True 比较:", SortableMoney(100, "USD") < SortableMoney(50, "EUR"),
      "<- 只比较裸的 cents，币种不同也不报错")
```

实际输出：

```
Money(cents=401, currency='USD')
跨币种相加: 币种不同：USD 与 EUR
order=True 比较: False <- 只比较裸的 cents，币种不同也不报错
```

**为什么。** 把币种和整数绑成一个对象，调用方就不会忘记币种；把 `from_decimal` 做成入口，舍入规则（这里是 `ROUND_HALF_UP`）只写在这一处。

**易错。** `@dataclass(order=True)` 会按字段顺序比较，`Money(100, "USD") < Money(50, "EUR")` 只比较裸的整数，不报错也没有意义。需要排序时，要么限定同币种，要么自己写 `__lt__` 并检查币种。
