---
id: craft-entity-vs-value-object-1-seat-is-a-value
node: craft.architecture.entity-vs-value-object
type: qa
step: 1
---
## Q
**实体 vs 值对象 · 座位被占了，这个状态该存在 Seat 上吗**｜架构

订座系统里，同一架飞机每天飞一班，座位图（12C、12D…）是同一份。很自然会写 `Seat(label, taken_by)`。周一有人订了 12C，周二的 12C 会怎样？应该怎样划分「椅子」和「谁占了椅子」？

## A
**要点。** 判据是：这个属性是它自己的，还是它「在某个上下文里」才有的？椅子的舱位、排号、字母是椅子自己的，不随航班变，它是值对象（value object，按内容相等、不可变、可随意共享）。「被谁占了」只在某一天某一班里才成立，属于那一班的状态，放进 `FlightInstance` 的座位图。放错就是同一份数据被很多班次共用，一个班次的变化泄漏给所有班次。

```python
# 错误：占用放在「椅子」上，而椅子是同一架飞机所有航班共用的
@dataclass
class SeatBad:                       # 错：占用写在共用的椅子上
    label: str
    taken_by: str | None = None

shared_layout = [SeatBad("12C")]                     # 同一架飞机的座位图
mon = tue = shared_layout                            # 周一、周二的两班共用它
mon[0].taken_by = "张三"                              # 周一订了 12C
print("错误：周二 12C 被占了？", tue[0].taken_by is not None)

# 正确：椅子是值（冻结、可共享），占用在每一班自己的座位图里
@dataclass(frozen=True, slots=True)
class Seat:                          # 对：椅子是冻结的值，可共享
    label: str

@dataclass
class FlightInstance:
    date: str
    seats: tuple[Seat, ...]
    occupied: dict[str, str] = field(default_factory=dict)   # 座位号 -> 订单号

layout = (Seat("12C"),)                              # 一份冻结的布局，所有班次共用
mon = FlightInstance("周一", layout)
tue = FlightInstance("周二", layout)
mon.occupied["12C"] = "张三"
print("正确：周二 12C 被占了？", "12C" in tue.occupied, "| 布局是同一个对象:", mon.seats is tue.seats)
try:
    layout[0].label = "99Z"
except Exception as e:
    print("共享的值改不动:", type(e).__name__)
```

周一订 12C 后，两种写法下周二的 12C 状态，以及试图改共享的椅子，实际输出：

```
错误：周二 12C 被占了？ True
正确：周二 12C 被占了？ False | 布局是同一个对象: True
共享的值改不动: FrozenInstanceError
```

**为什么。** 值对象冻结之后可以放心地让很多对象共享一份，省内存，也省去防御性拷贝；变化只发生在持有状态的实体里。

**易错。** 「椅子上写个 `is_free`」读起来最自然，错误也最隐蔽：只有单个航班时一切正常，第二个航班出现时才露出来。
