---
slug: parking-lot-system
kind: low-level-design
---

## Q
**停车场管理系统**｜低层设计

用你选择的编程语言设计并实现一个停车场管理系统：代码要求语法正确，但不会被实际运行。车辆入场时分配车位并领取停车票，离场时按停车时长计费、缴费、释放车位。常见的扩展：多种车型和多种车位（摩托、小型、大型、无障碍、电动车充电位）、多层、多个出入口、不同的计费规则、并发入场、车位显示牌、遗失票据。高级别面试官关注的是类的边界、扩展点和并发下的正确性。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 这题考的是把"变化点"隔离开：车位分配策略和计费规则都会变，所以做成两个可替换的策略；而车位的占用与释放是并发下唯一需要保护的共享状态，必须是原子操作，并且离场要先缴费成功才释放车位。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求（车型、车位类型、计费），定接口 |
| 8–13 分 | 类与职责：两个策略、门面、枚举加兼容表 |
| 13–45 分 | 写核心实现：兼容表、最近优先分配器、`ParkingLot` 的入场和离场 |
| 45–50 分 | 跑例子：分配顺序、满位、先缴费后释放、重复离场 |
| 50–60 分 | 追问：计费规则、重复车牌、显示牌、恢复和扩展 |

**需求。**
- 功能：
  1. 车辆入场：按车型找到合适的空车位，生成停车票（含入场时间、车位）。
  2. 车辆离场：凭票计算费用，缴费后释放车位。
  3. 查询各类车位的剩余数量；满位时拒绝入场。
  4. 支持多层、多种车位类型；摩托可以停小型位，但大型车不能停小型位。
  5. 遗失票据按最高日费处理。
- 非功能：
  - 并发：多个入口同时入场，同一个车位不能分给两辆车。
  - 扩展：新增车位类型、新的计费规则、新的分配策略，不改核心流程。
  - 假设规模：几千个车位，每秒数次进出，单机内存即可，状态可以由未结束的停车票重建。

**核心实体与接口。**
- 类与职责：
  - `VehicleType`、`SpotType` 枚举；`COMPAT` 表：每种车型按偏好顺序可使用的车位类型。
  - `Spot`：车位，持有层、类型、到入口的距离，是否被占用。
  - `Ticket`：停车票，含票号、车牌、车位、入场时间。
  - `SpotAllocator`（策略接口）：`allocate(vehicle_type)` 与 `release(spot)`；实现 `NearestFirstAllocator`，每种车位类型维护一个按距离排序的最小堆。
  - `FeePolicy`（策略接口）：`fee(entered, exited)`；核心里用最简单的 `HourlyFee`，阶梯计费 `TieredFee` 在逐步扩展里。
  - `ParkingLot`：对外门面，持有分配器、计费策略和未结束的票；`enter`、`exit`。
- 对外接口：`enter(plate, vehicle_type, now) -> Ticket`、`exit(ticket_id, now, pay) -> fee`；显示牌用的 `available()` 在逐步扩展里加。

用到的模式：策略模式（`SpotAllocator`、`FeePolicy`，两个变化最多的点）、门面（`ParkingLot` 隐藏分配与计费细节）、枚举加兼容表（新增车位或车型只改表）。原因：最常见的追问是"再加一种计费规则 / 再加电动车位"，策略和表让这类变化只增加代码，不修改已有流程。

**整体设计。**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 294">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<line x1="170" y1="36" x2="170" y2="53"/>
<line x1="170" y1="86" x2="170" y2="103"/>
<line x1="170" y1="136" x2="170" y2="153"/>
<line x1="170" y1="186" x2="170" y2="203"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="12" y="8" width="316" height="28" rx="3"/>
<rect x="12" y="58" width="316" height="28" rx="3"/>
<rect x="12" y="108" width="316" height="28" rx="3"/>
<rect x="12" y="158" width="316" height="28" rx="3"/>
<rect x="12" y="208" width="316" height="28" rx="3"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="170,58 167,52 173,52"/>
<polygon points="170,108 167,102 173,102"/>
<polygon points="170,158 167,152 173,152"/>
<polygon points="170,208 167,202 173,202"/>
</g>
<g fill="currentColor">
<text x="170" y="26" font-size="12">入口: enter(车牌, 车型)</text>
<text x="170" y="76" font-size="12">SpotAllocator: 最近优先堆</text>
<text x="170" y="126" font-size="12">Ticket: 车位 + 入场时间</text>
<text x="170" y="176" font-size="12">出口: FeePolicy 计费</text>
<text x="170" y="226" font-size="12">缴费成功 -> 释放车位</text>
</g>
<g style="fill:var(--dim,#6b7280)"><text x="170" y="252" font-size="11">分配与释放在同一把锁内</text></g>
<g style="fill:var(--dim,#6b7280)"><text x="170" y="268" font-size="11">离场幂等, 不重复释放</text></g>
</g></svg>
```
- 入场：向分配器取车位，生成票据，写入未结束票据表。
- 离场：查票据，调用计费策略算费，缴费成功后移除票据并释放车位；缴费失败时保持占用，用户可重试。

**核心实现。** 约 32 分钟，下面是全部要写的代码：车型与车位的兼容表、最近优先的分配器、简单计费、入场和离场。

```python
import heapq
import itertools
import math
from dataclasses import dataclass
from enum import Enum
from threading import Lock
from typing import Callable


class VehicleType(Enum):
    MOTORCYCLE = 1; CAR = 2; TRUCK = 3


class SpotType(Enum):
    SMALL = 1; REGULAR = 2; LARGE = 3


# 车型 -> 允许使用的车位类型，按偏好顺序（先试最合适的，省大位给大车）
COMPAT = {
    VehicleType.MOTORCYCLE: [SpotType.SMALL, SpotType.REGULAR, SpotType.LARGE],
    VehicleType.CAR: [SpotType.REGULAR, SpotType.LARGE],
    VehicleType.TRUCK: [SpotType.LARGE],
}


@dataclass(frozen=True)
class Spot:
    spot_id: str
    kind: SpotType
    distance: int              # 到最近出入口的距离，越小越优先


@dataclass
class Ticket:
    ticket_id: str
    plate: str
    spot: Spot
    entered_at: float          # 秒级时间戳


class LotFull(Exception): ...
class InvalidTicket(Exception): ...


class NearestFirstAllocator:   # 策略一：allocate(vt) / release(spot)，可替换
    """每种车位一个最小堆（按距离）。分配与释放都是 O(log n)，用一把锁保证原子性。"""
    def __init__(self, spots: list[Spot]) -> None:
        self._free: dict[SpotType, list] = {k: [] for k in SpotType}
        for s in spots:
            heapq.heappush(self._free[s.kind], (s.distance, s.spot_id, s))
        self._lock = Lock()

    def allocate(self, vt: VehicleType) -> Spot | None:
        with self._lock:       # 检查和取走在同一个临界区，杜绝同一车位分给两辆车
            for kind in COMPAT[vt]:
                if self._free[kind]:
                    return heapq.heappop(self._free[kind])[2]
            return None

    def release(self, spot: Spot) -> None:
        with self._lock:
            heapq.heappush(self._free[spot.kind], (spot.distance, spot.spot_id, spot))


class HourlyFee:               # 策略二：fee(进场时间, 离场时间) -> 分，可替换
    def fee(self, entered_at: float, exited_at: float) -> int:
        return math.ceil(max(0.0, exited_at - entered_at) / 3600) * 300   # 每小时 300 分，向上取整


class ParkingLot:
    def __init__(self, allocator: NearestFirstAllocator, policy: HourlyFee) -> None:
        self.allocator, self.policy = allocator, policy
        self._active: dict[str, Ticket] = {}   # 未结束的票；崩溃后可由它重建占用状态
        self._seq = itertools.count(1)

    def enter(self, plate: str, vt: VehicleType, now: float) -> Ticket:
        spot = self.allocator.allocate(vt)
        if spot is None:
            raise LotFull()
        t = Ticket(f"T{next(self._seq)}", plate, spot, now)
        self._active[t.ticket_id] = t
        return t

    def exit(self, ticket_id: str, now: float, pay: Callable[[int], bool]) -> int:
        t = self._active.get(ticket_id)
        if t is None:
            raise InvalidTicket()
        amount = self.policy.fee(t.entered_at, now)
        if amount and not pay(amount):
            raise InvalidTicket("缴费失败，车位保持占用")   # 先缴费成功，再释放车位
        if self._active.pop(ticket_id, None) is None:   # pop 是原子的：重复离场不会二次释放
            return amount
        self.allocator.release(t.spot)
        return amount
```

**运行。** 车位：`S1`（小，距离 1）、`R1`（普通，2）、`R2`（普通，5）、`L1`（大，3）；每小时 300 分：
- 摩托 A、小车 B、小车 C 依次入场，分到 `S1`、`R1`、`R2`；摩托 D 小位和普通位都满了，退到 `L1`。
- 再来一辆卡车或小车：抛 `LotFull`。
- A 停了 3601 秒，费用是 `600`（2 小时）；缴费回调返回 `False` 时抛 `InvalidTicket`，车位保持占用；缴费成功后再用同一张票离场抛 `InvalidTicket`，不会二次释放。
- A 离场后摩托 H 入场，拿到刚释放的 `S1`。
- 32 个线程抢最后一个普通位：只有 1 个成功。

**逐步扩展。**
1. 【追问再讲】阶梯计费：前 15 分钟免费，首小时 500 分，之后每小时 300 分，每天封顶 3000 分。传给 `ParkingLot` 替换 `HourlyFee`，流程不用改。停 600 秒、900 秒是 `0`，901 秒、3600 秒是 `500`，3601 秒、7200 秒是 `800`，满 24 小时是 `3000`，24 小时加 1 小时是 `3500`。

```python
class TieredFee:
    """前 15 分钟免费；首小时 500 分；之后每小时 300 分，向上取整；每天封顶 3000 分。"""
    def __init__(self, grace=15 * 60, first=500, hourly=300, day_cap=3000) -> None:
        self.grace, self.first, self.hourly, self.day_cap = grace, first, hourly, day_cap

    def fee(self, entered_at: float, exited_at: float) -> int:
        secs = max(0.0, exited_at - entered_at)
        if secs <= self.grace:
            return 0
        days, rest = divmod(secs, 86400)
        total = int(days) * self.day_cap
        if rest > 0:
            hours = math.ceil(rest / 3600)
            total += min(self.first + (hours - 1) * self.hourly, self.day_cap)
        return total
```

2. 【追问再讲】同一车牌不能重复入场：先占位，分配失败要回滚占位。

```python
# ParkingLot.__init__ 新增 self._plates: set[str] = set() 和 self._lock = Lock()；enter 改成
def enter(self, plate: str, vt: VehicleType, now: float) -> Ticket:
    with self._lock:
        if plate in self._plates:
            raise InvalidTicket("该车辆已在场内")
        self._plates.add(plate)            # 先占位，防止同一车牌并发重复入场
    spot = self.allocator.allocate(vt)
    if spot is None:
        with self._lock:
            self._plates.discard(plate)    # 分配失败要回滚占位
        raise LotFull()
    t = Ticket(f"T{next(self._seq)}", plate, spot, now)
    with self._lock:
        self._active[t.ticket_id] = t
    return t

# exit 里 pop 成功之后加一行：self._plates.discard(t.plate)
```

3. 【加分】车位显示牌：分配器暴露各类型剩余数量，显示牌定时读取或订阅变化，不影响主流程。

```python
# NearestFirstAllocator 新增：显示牌读取各类型剩余车位
def available(self) -> dict[SpotType, int]:
    with self._lock:
        return {k: len(v) for k, v in self._free.items()}
```

**深入。**
1. 【必讲】分配策略。
   - 随便找第一个空位：实现最简单，但用户要走很远。
   - 最近优先（选用）：每种车位一个按距离排序的堆，取走最近的空位 O(log n)；有多个出入口时，距离取到所有出入口的最小值，或每个入口一个堆。
   - 车型兼容：先试最合适的类型，再升级到更大的位置（摩托占小位优先，实在没有占普通位）；这是贪心，保证大车位尽量留给大车。停车规则是数据，不是行为，用兼容表比继承（Car 继承 Vehicle 再各自判断能停哪）更容易修改。
   - 不做的事：释放时不"合并"空位，也不重新分配已入场车辆。
2. 【必讲】并发和离场幂等。
   - 共享状态只有各类型的空位堆和未结束票据。分配器的"检查并取走"在一把锁内完成；不同车位类型可以用各自的锁降低争用，但跨类型的兼容顺序会引入多锁，初版一把锁足够，几千车位每秒数次进出毫无压力。
   - 离场的幂等：用 `pop` 的返回值判断是否第一次处理，避免重复释放同一车位（重复释放会让同一车位出现两次在堆里，随后被分给两辆车，这是最严重的 bug）。
3. 【必讲】为什么先缴费后释放：释放车位意味着可以再分配，若缴费失败而车位已释放，车辆仍在场内，会出现一个车位对应两辆车。缴费失败就抛异常，车位保持占用，用户可重试。
4. 【追问再讲】计费。
   - 把计费做成策略：按小时、阶梯、包天封顶、工作日与节假日差异、会员折扣都各是一个实现，或用组合（先基础费再折扣装饰器）。
   - 时间边界：免费时段、向上取整、跨天封顶要有明确定义并写测试；金额用整数分，不用浮点数。
   - 遗失票据：按最高日费收取，需要核验车牌（凭车牌与行驶证）。
5. 【追问再讲】状态恢复。
   - 进程重启后内存状态丢失：持久化未结束票据（数据库或日志），启动时遍历票据，把对应车位从空位堆里标记为占用，重建分配器。
   - 车位使用状态以票据为准，不单独存一份"占用标志"，避免两处状态不一致。
6. 【加分】扩展点。
   - 电动车充电位：新增车位类型和兼容表条目，车型增加"需要充电"属性；充电计费是另一个策略。
   - 预约车位：预留一批车位在预约时间段内不可分配，需要在分配器里增加预约表；或者把预约当作带到期时间的特殊票据。
   - 无障碍位：加类型，兼容表仅对持有证件的车辆开放。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 怎么测试：用注入的时间（`now` 参数）而不是读系统时钟；并发测试让多个线程抢最后一个车位，断言只有一个成功。
- 高并发入口怎么扩展：每层或每区一个分配器实例，入口优先使用本区，满了再借其他区；初版不需要。
- 这个设计支持多个停车场吗：`ParkingLot` 是实例而不是单例，多个实例各持有自己的分配器；全局注册表另议。

**级别期望。**
- 中级：车辆、车位、票据、停车场几个类，能完成入场和离场，算出费用。
- 高级：分配与计费的策略化、车型与车位的兼容表、并发下车位唯一分配、先缴费再释放。
- 资深（staff）：状态恢复、多入口多层的分配、离场幂等的论证、时间注入的可测试性、扩展（预约、充电）如何不改核心代码，以及并发粒度的取舍。

**先修概念。** [[hi-low-level-design-in-a-hurry-delivery|答题框架（Delivery Framework）]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-low-level-design-in-a-hurry-design-principles|设计原则]]、[[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-concurrency-intro|并发入门]]

**同类题。** [[solution-parking-lot]]（本库完整题解）、[[hi-low-level-design-problem-breakdowns-parking-lot|停车场]]、[[solution-amz-parking-fees]]、[[solution-amazon-locker]]
