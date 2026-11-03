---
id: craft-entity-vs-value-object-4-equality-in-python
node: craft.architecture.entity-vs-value-object
type: qa
step: 4
---
## Q
**实体 vs 值对象 · 在 Python 里怎样把「实体」和「值」落到 dataclass 上**｜架构

订单（Booking）会被改状态，金额（Money）不会。两者都写成 `@dataclass`，默认的 `eq=True` 会带来什么？订单放进字典做键或放进集合时会出什么事？应该分别用哪个参数组合？

## A
**要点。** 实体靠身份（identity）区分，状态随时变；值靠内容区分，从不变。可变且按内容相等的类是最危险的组合：内容一变，相等和哈希的结果都跟着变。因此实体用 `@dataclass(eq=False)`：保持默认的对象身份比较和哈希；值用 `@dataclass(frozen=True, slots=True)`：内容相等、可哈希、只读。

```python
@dataclass                        # eq=True 且可变：__hash__ 被置为 None
class BookingBad:
    ref: str
    state: str = "HELD"

a, b = BookingBad("B1"), BookingBad("B1")
print("内容相同就相等:", a == b)
try:
    {a: 1}
except TypeError as e:
    print("放不进字典:", type(e).__name__)

@dataclass(eq=False)              # 实体：身份相等，按对象哈希，状态随便变
class Booking:
    ref: str
    state: str = "HELD"

a, b = Booking("B1"), Booking("B1")
seen = {a: "x"}
a.state = "PAID"                  # 状态变了，哈希不变，还能找到
print("改状态后还在字典里:", a in seen, "| 两个对象相等:", a == b)

@dataclass(frozen=True, slots=True)
class Money:                      # 值：内容相等，可哈希，可共享
    cents: int
    cur: str

print("值对象:", Money(500, "USD") == Money(500, "USD"), {Money(500, "USD"): 1}[Money(500, "USD")])
```

实际输出（`BookingBad("B1") == BookingBad("B1")` 及放进字典，改状态后的 `Booking`，两个相同内容的 `Money` 作键）：

```
内容相同就相等: True
放不进字典: TypeError
改状态后还在字典里: True | 两个对象相等: False
值对象: True 1
```

**为什么。** 3.11+ 里，`eq=True` 且不冻结的 dataclass 把 `__hash__` 设成 `None`，所以不能当字典键；这是标准库在逼你做选择：要么内容相等并冻结，要么身份相等。

**代价。** 实体按身份比较，两个 ref 相同的订单对象不相等，需要「是不是同一张订单」时自己比 `ref`，或者用 `dict[ref, Booking]` 保证全局只有一个对象。
