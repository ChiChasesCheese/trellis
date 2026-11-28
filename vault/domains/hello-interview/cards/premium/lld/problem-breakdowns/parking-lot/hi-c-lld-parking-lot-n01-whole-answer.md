---
id: hi-c-lld-parking-lot-n01-whole-answer
node: lld.problem-breakdowns.parking-lot.notes
type: qa
step: 1
---
## Q
**停车场 · 完整解答（一张卡）**｜摘要 · 必会

设计一个停车场系统：支持摩托车、汽车、大型车三种车；进场时系统自动分配兼容的空车位并发一张票；出场时凭票计算按小时（不足一小时按一小时）的费用并释放车位。给出需求、实体与接口、整体设计、关键实现、深入问题和各级别的期望。

## A
**一句话。** 三个类：`ParkingLot` 是唯一的入口，管分配、票、计费和"哪些车位被占"；`ParkingSpot` 只有编号和类型；`Ticket` 是不可变的停车记录。车辆本身不建类，只是一个分类枚举。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–5 分 | 澄清：车型、票、计费、满了和坏票怎么办 |
| 5–10 分 | 实体：车辆为什么只是枚举 |
| 10–25 分 | 类设计：占用状态放哪、计费放哪 |
| 25–45 分 | 实现：`enter`、`exit`、找车位、算费 |
| 45–50 分 | 走一遍进场、出场、重复出场、满场 |
| 50–60 分 | 追问：多楼层、按车型定价、多入口并发 |

**需求。**
- 功能：
  - 三种车型，进场自动分配兼容的车位，并发票
  - 出场凭票：校验、按时间计费（按小时，向上取整）、释放车位
  - 所有车型同一个小时费率
  - 没有兼容车位拒绝进场；票无效或已用过拒绝出场
- 范围外：支付、道闸硬件、摄像头、界面、预约

**实体与接口。**
- **对外只有两个方法：** `ParkingLot(spots, hourly_cents)`：`enter(vehicle) -> Ticket`、`exit(ticket_id) -> 费用（分）`；除此之外不暴露内部状态
- `ParkingSpot`：编号、类型（固有属性）
- `Ticket`：票号、车位编号、车型、进场时间；创建后不再改变
- 车位类型与车型各用一个枚举，虽然现在取值一样

**整体设计。**
1. **进场找车位造票：** 扫描车位，找类型兼容且不在占用集合里的第一个→加入占用集合→造票→存进活跃票表→返回票
2. **出场取票算费：** 从票表取出并删除该票（取不到就是无效或已用）→从占用集合移除车位→按进场与当前时间算费
3. **两份状态同进同出：** 占用集合与活跃票表是 `ParkingLot` 里的两份状态，必须同进同出

**核心实现。** 约 85 行：

```python
import threading
import time
import uuid
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Optional

HOUR_MS = 3_600_000


class SpotType(Enum):
    MOTORCYCLE = auto()
    CAR = auto()
    LARGE = auto()


class VehicleType(Enum):                 # 与 SpotType 同名但语义不同：车 != 位
    MOTORCYCLE = auto()
    CAR = auto()
    LARGE = auto()


class LotFull(Exception): ...
class BadTicket(Exception): ...


@dataclass(frozen=True)
class ParkingSpot:                       # 只有固有属性；占用不在这里
    id: str
    type: SpotType


@dataclass(frozen=True)
class Ticket:                            # 不可变记录；存 spot_id 而不是车位对象
    id: str
    spot_id: str
    vehicle: VehicleType
    entered_ms: int


# 车型 -> 可停的车位类型（按偏好排序）。今天一对一；摩托车借用汽车位只需改这张表
FITS = {VehicleType.MOTORCYCLE: (SpotType.MOTORCYCLE,),
        VehicleType.CAR: (SpotType.CAR,),
        VehicleType.LARGE: (SpotType.LARGE,)}


class ParkingLot:
    def __init__(self, spots: list[ParkingSpot], hourly_cents: int,
                 clock_ms: Callable[[], int] = lambda: int(time.time() * 1000)) -> None:
        self._spots = list(spots)
        self._rate = hourly_cents        # 金额用整数分，不用浮点
        self._clock = clock_ms           # 注入时钟，测试可快进
        self._occupied: set[str] = set()                 # 关系状态：被某张票占着的车位
        self._tickets: dict[str, Ticket] = {}            # 活跃票，按 id 查
        self._lock = threading.Lock()                    # 多入口时保护占用集合和票表

    def enter(self, v: VehicleType) -> Ticket:
        with self._lock:                 # 查找车位与占用车位必须是不可分的一步
            spot = self._find(v)
            if spot is None:
                raise LotFull(v.name)    # 拒绝时尚未改动任何状态
            t = Ticket(uuid.uuid4().hex, spot.id, v, self._clock())   # 先造票，再改状态
            self._occupied.add(spot.id)
            self._tickets[t.id] = t
            return t

    def exit(self, ticket_id: str) -> int:
        with self._lock:
            t = self._tickets.pop(ticket_id, None)   # 验证与作废一步完成：重复出场必然失败
            if t is None:
                raise BadTicket()
            self._occupied.discard(t.spot_id)
            return self._fee(t.entered_ms, self._clock())

    def _find(self, v: VehicleType) -> Optional[ParkingSpot]:
        for want in FITS[v]:
            for s in self._spots:
                if s.type is want and s.id not in self._occupied:
                    return s
        return None

    def _fee(self, start: int, end: int) -> int:
        hours = -(-max(end - start, 0) // HOUR_MS)      # 整数向上取整，不经过浮点
        return max(hours, 1) * self._rate               # 至少收一小时
```

**运行。** 三个车位 A 摩托、B 汽车、C 大型，费率 500 分：
- 汽车进场分到 B；再进一辆汽车→`LotFull`，状态没变
- 2.5 小时后出场：向上取整为 3 小时，1500 分；同一张票再出→`BadTicket`

**深入。**
1. 【必讲】实体：车辆在系统外，只用它的类型，建枚举而非类；票要建类，它是系统自己创建的会话记录
2. 【必讲】占用状态放哪：放在车位上（有冗余）、从票推算（最干净）、在 Lot 里维护一个占用集合（有索引的折中）；这里占用是"被票分配"，属于关系状态
3. 【必讲】计费放哪：不放 `Ticket`（让记录变成计算器），放 `ParkingLot`；只有真有多套定价规则才抽策略
4. 【必讲】金额用整数分，不用浮点
5. 【追问再讲】多楼层：在 Lot 和车位之间加 `ParkingFloor`，票结构不变
6. 【追问再讲】按车型定价：费率表 `车型->费率`
7. 【加分】多入口并发：粗粒度锁就够，细粒度是乐观认领加重试

**级别期望。**
- 中级：职责分离不靠引导；车辆是枚举；处理满场、无效票、重复出场；能解释为什么票表用字典、计费为什么在 Lot 里
- 高级：主动讲占用状态的几种放法和理由、两个枚举为何分开；自己发现边界；扩展时先讲简单方案再说何时上模式
