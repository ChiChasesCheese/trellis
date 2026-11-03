---
id: craft-kw-only-positional-only-3-dataclass-kw-only
node: craft.idioms.kw-only-positional-only
type: qa
step: 3
---
## Q
**参数形态 · 十个字段的记录为什么用 dataclass(kw_only=True)**｜写法

订单 `Booking` 有十个字段：必填的 id、旅客、票价，加上一堆带默认值的状态字段。用普通 `@dataclass` 时，字段的顺序必须是必填在前、默认值在后，一旦想把相关字段放在一起就报错；而实际的构造点全都在用关键字。`kw_only=True` 解决了什么？

## A
**要点。** 普通数据类的 `__init__` 参数顺序等于字段顺序，而 Python 不允许有默认值的参数排在没有默认值的前面，所以声明顺序被这条规则扭曲。`kw_only=True`（Python 3.10 起）让所有字段变成仅关键字：声明顺序只表达「读起来合理」，不再决定构造方式；位置传参被禁止，十个字段的记录不会再有人传错位。

```python
from dataclasses import dataclass

try:
    @dataclass
    class A:
        id: str
        status: str = "held"
        passenger: str                              # 没默认值的字段不能排在有默认值的后面
except TypeError as e:
    print("TypeError:", e)

@dataclass(kw_only=True, slots=True)
class Booking:
    id: str
    passenger: str
    fare: int
    status: str = "held"
    refunded: int = 0

b = Booking(id="b1", passenger="ann", fare=500)    # 关键字构造：字段顺序不再是 API
print(b)
try:
    Booking("b1", "ann", 500)
except TypeError as e:
    print("TypeError:", e)
```

实际输出（Python 3.14；报错文字在 3.11 里略有不同）：

```
TypeError: non-default argument 'passenger' follows default argument 'status'
Booking(id='b1', passenger='ann', fare=500, status='held', refunded=0)
TypeError: Booking.__init__() takes 1 positional argument but 4 were given
```

**为什么。** 字段超过三四个时，调用点用关键字几乎是必然的；让语言强制，比靠约定可靠。字段顺序也不再是公共接口，增减字段不会让位置调用的人错位。

**代价。** 两三个字段的小值对象（坐标、范围）不要这样：`Point(1, 2)` 比 `Point(x=1, y=2)` 自然得多，也能配合 `match` 的位置模式。
