---
slug: dasher-payout
kind: low-level-design
---
## Q
**设计配送员报酬计算（按配送事件）**｜低层设计

设计一个类或接口，根据外部服务提供的配送事件，计算一位配送员（Dasher）的总报酬。每一单有若干带时间戳的事件（已接单、已送达、已取消）；报酬是基础费率，外加配送员同时在途多单时的加成倍率。系统一次只处理一位配送员，依赖的外部服务用模拟数据。常见追问：按分钟计费、取消的单付不付、高峰时段倍率翻倍、按结算周期汇总，以及"怎样算得高效"。面试官看重的是：同时在途的单数怎么高效算出来、金额的精度和舍入、以及接口和数据模型是否清晰。

给出完整解答：需求、核心实体与接口、整体设计、核心实现、逐步扩展、深入问题、取舍、不同级别的期望。

## A
**一句话。** 只保存事实（每单的接单时间、结束时间和结果），钱每次现算：按接单时间排序，用一个按结束时间排的最小堆数出"接单那一刻还有几单在途"，据此取倍率；金额用精确分数计算，每单只在最后舍入一次。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清语义：同时在途怎么算、取消的单付不付、倍率怎么随在途数增长；定接口 |
| 8–14 分 | 数据模型（事件、订单、费率方案）；说出"先排序、再用堆数在途数"的算法 |
| 14–45 分 | 写核心实现：事件配对、按接单时刻的在途数计价、`Payroll` |
| 45–50 分 | 跑例子：单单、重叠、同刻结束、取消、非法事件 |
| 50–60 分 | 追问：按分钟计费、高峰窗口、结算周期、规模与时区 |

**需求。**
- 功能：
  - 输入：某位配送员的事件列表 `(delivery_id, status, at)`，`status` 是 `ACCEPTED`、`DELIVERED`、`CANCELLED`；事件可以乱序给出；
  - 每一单恰有一个接单事件和一个结束事件（送达或取消），结束不早于接单，否则抛 `InvalidEventsError`；
  - 每单报酬 = 基础报酬 x 倍率，倍率由接单那一刻"仍在途的其他单数"决定：0 单是 1 倍，之后按费率方案里的档位递增，超过最高档按最高档；
  - 取消的单付不付，由方案的开关 `pay_cancelled` 决定，默认不付；取消的单在取消之前仍算"在途"；
  - 在 `t` 时刻结束的单，不算与在 `t` 时刻接的单同时在途。
- 非功能：
  - 金额用精确算术，不用 `float`；每单只舍入一次，到分，0.5 进位；
  - 外部服务注入，测试不访问网络，没有 `sleep`；
  - 算法 O(n log n)，不是对每一单扫一遍全部订单的 O(n²)。例如一个结算周期内一位配送员有 n = 1,000 单（假设）：逐对比较约 1,000 x 1,000 = 1,000,000 次，排序加堆约 1,000 x log2(1,000) ≈ 10,000 次。

**核心实体与接口。**
- `Event`：外部服务给的事实，`@dataclass(frozen=True, slots=True)`；
- `Delivery`：配对后的一单，`accepted`、`ended`、`delivered`（假就是取消）；
- `PayPlan`：基础报酬、倍率档位 `tiers`（在途数到倍率）、`pay_cancelled`；构造时把档位字典拷成只读视图；
- `to_deliveries(events)`：配对并校验，按接单时间排序；
- **price_by_acceptance 纯函数：** `price_by_acceptance(plan, deliveries)`：纯函数，返回 `{订单号: 金额}`；
- **Payroll 注入 fetch_events：** `Payroll(plan, fetch_events)`：`delivery_pays(driver_id)`、`payout(driver_id)`，外部服务通过 `fetch_events` 注入。

**整体设计。** 数据只往一个方向流：
1. **fetch_events 只取回事件：** `fetch_events(driver_id)` 取回事件，不排序、不去重，也不保存；
2. `to_deliveries` 按订单号归并事件，校验后按 `(接单时间, 订单号)` 排序；
3. `price_by_acceptance` 顺序扫描：堆里放在途订单的结束时间，每到一个新订单，先把结束时间不晚于它接单时间的订单弹出，堆的大小就是接单时的在途数；
4. 取档位倍率，乘基础报酬，每单舍入一次，加总得到 `payout`。

**核心实现。** 约 30 分钟，下面是全部要写的代码：

```python
import heapq
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from types import MappingProxyType


class Status(Enum):
    ACCEPTED = "accepted"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class Event:                                  # 外部服务给的事实：哪一单、什么状态、什么时候
    delivery_id: str
    status: Status
    at: datetime


class PayrollError(Exception): ...
class InvalidEventsError(PayrollError): ...


@dataclass(frozen=True, slots=True)
class PayPlan:
    base: Decimal                             # 每单基础报酬
    tiers: Mapping[int, Decimal] = field(default_factory=lambda: {0: Decimal(1)})  # 接单时已在途的单数 -> 倍率
    pay_cancelled: bool = False               # 取消的单付不付：要在需求里问清

    def __post_init__(self) -> None:
        object.__setattr__(self, "tiers", MappingProxyType(dict(self.tiers)))  # 拷成只读视图，调用方之后改原字典不影响
        if self.base < 0 or sorted(self.tiers) != list(range(len(self.tiers))) or any(m <= 0 for m in self.tiers.values()):
            raise ValueError("base >= 0, tiers keyed 0..n with positive multipliers")

    def multiplier(self, ongoing: int) -> Decimal:
        return self.tiers[min(ongoing, len(self.tiers) - 1)]    # 超过最高档按最高档


@dataclass(frozen=True, slots=True)
class Delivery:
    id: str
    accepted: datetime
    ended: datetime
    delivered: bool                           # False 就是取消


def to_deliveries(events: Iterable[Event]) -> list[Delivery]:
    """把事件对成订单，按接单时间排序。每单恰有一个接单事件和一个结束事件，结束不早于接单。"""
    by_id: dict[str, dict[Status, datetime]] = {}
    for e in events:
        slot = by_id.setdefault(e.delivery_id, {})
        if e.status in slot:
            raise InvalidEventsError(f"{e.delivery_id}: duplicate {e.status.name}")
        slot[e.status] = e.at
    out = []
    for did, slot in by_id.items():
        ends = [s for s in (Status.DELIVERED, Status.CANCELLED) if s in slot]
        if Status.ACCEPTED not in slot or len(ends) != 1 or slot[ends[0]] < slot[Status.ACCEPTED]:
            raise InvalidEventsError(f"{did}: needs one ACCEPTED then one DELIVERED or CANCELLED")
        out.append(Delivery(did, slot[Status.ACCEPTED], slot[ends[0]], ends[0] is Status.DELIVERED))
    return sorted(out, key=lambda d: (d.accepted, d.id))


def _cents(x: Fraction) -> Decimal:
    """四舍五入（0.5 进位）到分，每单只在最后做一次。"""
    return Decimal(int(x * 100 + Fraction(1, 2))).scaleb(-2)


def price_by_acceptance(plan: PayPlan, deliveries: list[Delivery]) -> dict[str, Decimal]:
    """纯函数：每单的钱 = 基础报酬 x 接单那一刻的在途数对应的倍率。deliveries 已按接单时间排好。"""
    pays, ongoing = {}, []                    # ongoing：最小堆，放在途订单的结束时间
    for d in deliveries:
        while ongoing and ongoing[0] <= d.accepted:
            heapq.heappop(ongoing)            # 惰性弹出：时间只往前走，已结束的不会再回来；同刻结束不算同时在途
        multiplier = plan.multiplier(len(ongoing))
        heapq.heappush(ongoing, d.ended)      # 取消的单在取消前也占着配送员
        paid = d.delivered or plan.pay_cancelled
        pays[d.id] = _cents(Fraction(plan.base) * Fraction(multiplier)) if paid else Decimal("0.00")
    return pays


class Payroll:
    def __init__(self, plan: PayPlan, fetch_events: Callable[[str], Iterable[Event]]) -> None:
        self._plan, self._fetch = plan, fetch_events          # 外部服务注入：测试里换成假数据

    def delivery_pays(self, driver_id: str) -> dict[str, Decimal]:
        return price_by_acceptance(self._plan, to_deliveries(self._fetch(driver_id)))   # 存事实、现算钱

    def payout(self, driver_id: str) -> Decimal:
        return sum(self.delivery_pays(driver_id).values(), Decimal("0.00"))
```

**运行。** 基础报酬 10，档位 `{0: 1, 1: 1.5, 2: 2}`：
- 一单 10:00 接、10:30 送达：`payout` 是 `10.00`；
- `D1` 10:00–10:40、`D2` 10:10–10:30、`D3` 10:20–10:50、`D4` 10:30–11:00，都送达：`D1` 接单时没有在途，`10.00`；`D2` 时有 1 单，`15.00`；`D3` 时有 2 单，`20.00`；`D4` 在 10:30 接单，`D2` 恰好在 10:30 结束，不算同时在途，在途的只有 `D1`、`D3`，所以 `20.00`；合计 `65.00`，事件顺序反过来传结果不变；
- `D2` 改成 10:10–10:20 取消：默认不付，`D2` 为 `0.00`；`pay_cancelled=True` 时按接单时的在途数付 `15.00`；
- 缺结束事件、结束早于接单、同一单既送达又取消，都抛 `InvalidEventsError`；档位的键不是从 0 开始的连续整数，`PayPlan` 抛 `ValueError`。

**逐步扩展。**
1. 【追问再讲】按分钟计费：触发"按配送员花的分钟数付钱，倍率按重叠时段算"。把所有接单、结束时间点排序，相邻两个时间点之间在途的集合不变，每一单在这段里拿"每分钟单价 x 重叠倍率 x 秒数 / 60"。全程用 `Fraction`，最后每单舍入一次。

```python
from datetime import timedelta
from itertools import pairwise


class Payroll:  # 只列出新增或替换的方法
    def minute_pays(self, driver_id: str, per_minute: Decimal) -> dict[str, Decimal]:
        """按分钟计费：在途的每一单每分钟拿 per_minute x 重叠倍率。"""
        ds = to_deliveries(self._fetch(driver_id))
        exact = dict.fromkeys((d.id for d in ds), Fraction(0))
        points = sorted({t for d in ds for t in (d.accepted, d.ended)})
        for a, b in pairwise(points):                      # 相邻两个事件点之间，在途的集合不变
            active = [d for d in ds if d.accepted <= a and b <= d.ended]
            if not active:
                continue
            rate = Fraction(per_minute) * Fraction(self._plan.multiplier(len(active) - 1))
            seconds = Fraction((b - a) // timedelta(microseconds=1), 10**6)
            for d in active:
                if d.delivered or self._plan.pay_cancelled:
                    exact[d.id] += rate * seconds / 60     # 全程精确的分数，最后每单才舍入一次
        return {i: _cents(x) for i, x in exact.items()}
```

2. 【追问再讲】高峰窗口：触发"午晚高峰报酬翻倍"。在每个窗口的边界处把时间点再切开（可能跨天），每一小段取中点判断落在哪个窗口里，用该窗口的倍率，窗口边界属左属右都不用操心。窗口每天重复、左闭右开，`end == time(0)` 表示到午夜，跨午夜的窗口拆成两个。

```python
from collections.abc import Sequence
from datetime import date, time


@dataclass(frozen=True, slots=True)
class PeakWindow:
    """每天重复的高峰时段 [start, end)；end == time(0) 表示到当天午夜，跨午夜的窗口拆成两个。"""
    start: time
    end: time
    multiplier: Decimal

    @property
    def end_seconds(self) -> int:
        return 86400 if self.end == time(0) else _secs(self.end)

    def covers(self, t: time) -> bool:
        return _secs(self.start) <= _secs(t) < self.end_seconds


def _secs(t: time) -> int:
    return t.hour * 3600 + t.minute * 60 + t.second


def _at(day: date, seconds: int, like: datetime) -> datetime:
    """day 当天第 seconds 秒，时区与 like 相同；86400 秒就是第二天零点。"""
    return datetime.combine(day, time(0), tzinfo=like.tzinfo) + timedelta(seconds=seconds)


def _check_peaks(peaks: Sequence[PeakWindow]) -> None:
    ordered = sorted(peaks, key=lambda w: _secs(w.start))
    if any(w.end_seconds <= _secs(w.start) or w.multiplier <= 0 for w in ordered):
        raise ValueError("bad peak window")
    if any(a.end_seconds > _secs(b.start) for a, b in pairwise(ordered)):
        raise ValueError("peak windows overlap")


class Payroll:  # 只列出新增或替换的方法
    def minute_pays(self, driver_id: str, per_minute: Decimal, peaks: Sequence[PeakWindow] = ()) -> dict[str, Decimal]:
        _check_peaks(peaks)
        ds = to_deliveries(self._fetch(driver_id))
        exact = dict.fromkeys((d.id for d in ds), Fraction(0))
        points = {t for d in ds for t in (d.accepted, d.ended)}
        if points:                                         # 在每个高峰窗口的边界处再切一刀（可能跨天）
            lo, hi = min(points), max(points)
            for k in range((hi.date() - lo.date()).days + 1):
                day = lo.date() + timedelta(days=k)
                for w in peaks:
                    points |= {c for c in (_at(day, _secs(w.start), lo), _at(day, w.end_seconds, lo)) if lo < c < hi}
        for a, b in pairwise(sorted(points)):
            active = [d for d in ds if d.accepted <= a and b <= d.ended]
            if not active:
                continue
            mid = a + (b - a) / 2                          # 取小段中点判断落在哪个窗口：边界属左属右都不用操心
            peak = next((w.multiplier for w in peaks if w.covers(mid.time())), Decimal(1))
            rate = Fraction(per_minute) * Fraction(peak) * Fraction(self._plan.multiplier(len(active) - 1))
            seconds = Fraction((b - a) // timedelta(microseconds=1), 10**6)
            for d in active:
                if d.delivered or self._plan.pay_cancelled:
                    exact[d.id] += rate * seconds / 60
        return {i: _cents(x) for i, x in exact.items()}
```

3. 【加分】结算周期：触发"按周汇总"。整单记入结束时间落在 `[start, end)` 内的那一期，不按每段发生的时间拆；价格仍然只算一遍。

```python
class Payroll:  # 只列出新增或替换的方法
    def payout_between(self, driver_id: str, start: datetime, end: datetime) -> Decimal:
        """结算周期 [start, end)：整单记入结束时间落在周期内的那一期，不按每段发生的时间拆。"""
        ds = to_deliveries(self._fetch(driver_id))        # 事实只取一次
        pays = price_by_acceptance(self._plan, ds)
        return sum((pays[d.id] for d in ds if start <= d.ended < end), Decimal("0.00"))
```

**运行（逐步扩展）。**
- 按分钟，每分钟单价 0.10，档位 `{0: 1, 1: 1.5}`：`D1` 10:00–10:40、`D2` 10:10–10:30，其中 10:10–10:30 两单重叠，倍率 1.5。`D1` = 10 x 0.10 + 20 x 0.15 + 10 x 0.10 = `5.00`，`D2` = 20 x 0.15 = `3.00`；
- 高峰 11:00–14:00 倍率 1.5，一单 10:50–11:10，每分钟 0.25：0.25 x (10 + 10 x 1.5) = `6.25`；没有窗口是 `5.00`；
- 跨午夜的一单 23:50–00:10，窗口 23:00–24:00 倍率 2、00:00–01:00 倍率 3，每分钟 1：10 x 2 + 10 x 3 = `50.00`；窗口互相重叠或 `start >= end` 抛 `ValueError`；
- 结算周期：`A` 9:30 结束，`B` 10:30 结束，`C` 11:00 结束，周期 [10:00, 10:45) 只统计 `B`，`10.00`；
- 另外做了两组随机对照：堆的写法对照"逐个数在途"的 O(n²) 暴力写法 500 组一致；分钟计费对照"一分钟一分钟累加"的暴力写法 300 组一致（含高峰窗口和跨天）。

**深入。**
1. 【必讲】存事实、现算钱：
   - 不要每收到一个事件就往余额里累加：遇到乱序、重复、更正就得回滚旧账；现算的写法只要事实表对，钱就对；
   - 代价是每次查询都重新算；假设一位配送员一个周期只有几百单，这个代价可以忽略，要规模化时再加缓存或预聚合；
   - 事实 `Event`、`Delivery` 都是 `frozen=True, slots=True` 的值对象，`price_by_acceptance` 是纯函数，`Payroll` 只是取数据加调用（纯函数核心，外壳注入依赖）。
2. 【必讲】接单时在途几单，用排序加最小堆：
   - 订单按接单时间排好，扫描时间只往前走，所以结束时间不晚于当前接单时间的订单永远不会再有效，可以在堆顶发现时顺手弹出（惰性删除）；堆里每个订单最多进出一次，整体 O(n log n)；
   - 边界：堆里存的是"仍在途"的订单，判断条件是 `结束时间 <= 接单时间` 就弹出，所以同刻结束不算同时在途；取消的单在取消那一刻之前还占着配送员；
   - 放弃"对每一单扫描全部订单"，那是 O(n²)；同一时刻接多单时按订单号排序，保证结果与事件到达顺序无关。
3. 【必讲】金额精度与舍入：
   - 不用 `float`，二进制小数表示不了 0.1；也不让 `Decimal` 做 `/ 60`，循环小数会让四舍五入的边界差一位；中间量用 `Fraction` 精确计算，最后才转成 `Decimal` 到分；
   - 每单只舍入一次。例如三段各 0.125：每段先舍入成 0.13 得 0.39，整单先加得 0.375 再舍入是 0.38；
   - 舍入函数 `_cents` 用 `int(x * 100 + Fraction(1, 2))` 实现 0.5 进位（金额非负），整个过程没有浮点数。
4. 【追问再讲】先把语义问清，因为同一个问题有好几种变体：
   - 倍率按"接单那一刻在途数"（核心）还是按"重叠时段的分钟"（逐步扩展 1）；
   - 取消的单付不付、取消前的时间算不算在途；
   - 无并发加成、每单固定费率的变体最简单：每单固定金额，取消与否只影响一个开关，总额是 O(n) 求和，不需要排序和堆。
5. 【追问再讲】`PayPlan` 不可变：`tiers` 在 `__post_init__` 里拷成 `MappingProxyType`，调用方之后改自己的字典不会影响已建好的方案；直接保存传入的字典，等于把可变状态交给了别人。
6. **【追问再讲】切段取中点与 pairwise：** 切段取中点与 `pairwise`：
   - 相邻时间点两两配对用 `itertools.pairwise`，比 `zip(xs, xs[1:])` 少一次切片拷贝，意图也更直接；
   - 取小段中点判断所在窗口；逐分钟循环既慢，又在秒级精度上不准。
7. 【加分】结算周期归属：整单记入结束那一天所在的周期；放弃"每段按发生时间分别记入各自的周期"，那样同一单会被拆到两个周期，对账和配送员看到的单据都对不上。代价是跨天的单在结束那天一次性入账。
8. 【加分】时区与夏令时：事件时间统一成带时区的绝对时间，高峰窗口按订单所在地的本地时间判断；夏令时那天"一小时"可能出现两次或不存在，所以要在本地日历日上切段，而不是在 UTC 上加 24 小时。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 外部服务给了重复事件：相同内容的重复可以去重，内容不同就是冲突，应报错而不是悄悄覆盖；核心里重复一律抛 `InvalidEventsError`，先说清再决定。
- 订单还没结束（只有接单）：核心当作非法输入；要支持就给它一个极大的结束时间，扫描时它一直留在堆里。
- 想按单量给奖励（完成 10 单加 5 元）：奖励是 `payout` 之上的规则，作为独立的奖励策略对订单列表求值，不要写进 `price_by_acceptance`。
- 多个服务并发上报：事件按 `(delivery_id, status)` 幂等写入，计算只读快照。
- 数据量大了：事实表按配送员和结束时间建索引，周期汇总按日预聚合，更正事件作废对应日的预聚合。

**级别期望。**
- 中级：核心实现通过，事件配对与校验正确，能数出接单时的在途数，哪怕 O(n²)。
- 高级：排序加堆的 O(n log n) 算法，同刻结束、取消的边界；金额精确算术且只舍入一次；外部服务注入，纯函数核心。
- 资深/专家：按分钟计费与高峰切段（中点判断，`pairwise`）；结算周期的归属取舍；时区与夏令时；事实表的规模化与预聚合；奖励策略的分层。

**先修概念。**
- [[hi-low-level-design-in-a-hurry-delivery|答题框架]]
- [[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]
- [[hi-low-level-design-in-a-hurry-design-principles|设计原则]]
- [[hi-system-design-core-concepts-data-modeling|数据建模]]

**同类题。**
- [[solution-food-delivery|设计题解：外卖配送]]
- [[solution-digital-wallet|设计题解：数字钱包]]
- [[solution-amz-parking-fees|设计题解：停车计费]]
- [[solution-amz-aws-billing|设计题解：AWS 计费]]
