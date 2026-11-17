"""活动推荐规则修复（Event Campaigns）：待修的服务（规则与推荐器里有缺陷，数据类型是固定的）。

产品规则（编号即测试编号；全部时间都是带时区的 UTC，一周从周一到周日，价格是整数美分）：

1. 出发点：客户的 `location` 有值就用它；否则取 `home_city` 的坐标（位置服务认识这个城市才行）；否则没有出发点。
2. `within_miles(m)`：有出发点、活动城市有坐标、且两点距离 ≤ m（含边界）才匹配；缺任何一样都不匹配，也不抛异常。
3. `in_metro_area()`：活动在客户家所在城市，或在与它直接相邻的城市（邻接不传递）；没有 `home_city` 就谁也不匹配。
4. `within_days(d)`：活动开始时间 ∈ [now, now + d×24 小时]，两端都含；已经开始的不算。
5. `this_weekend()`：开始时间 ≥ now，且 ∈ [周六 00:00, 下周一 00:00)；周六、周日指正在过的这个周末，周一到周五指即将到来的那个。
6. `price_under(c)`：至少有一张票同时满足"数量 > 0"和"价格严格小于 c"。
7. `all_of(*r)`：全部匹配才匹配，没有规则时匹配一切；`any_of(*r)`：任一匹配就匹配，没有规则时什么都不匹配。
   可以嵌套，也能装下别处写的、带 `matches(event, context)` 的对象。
8. 规则只看它收到的 `event` 与 `context`：同一个规则对象服务多个客户、多个活动、多次调用，答案互不影响。
9. `recommend`：可推荐活动 = 开始时间 ≥ now 且至少有一张数量 > 0 的票，按 (开始时间, id) 排序。
10. 逐级尝试：第一个至少匹配一个可推荐活动的级别给出结果（它的匹配项，保持顺序，最多 `limit` 个），后面的级别不再看；先匹配、后截断。
11. 没有任何级别命中时，对每一位客户都返回可推荐活动的前 `limit` 个；只有可推荐活动为空时结果才为空。
"""

from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Protocol

# ---- models:begin ----
EARTH_RADIUS_MILES = 3958.8


@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float


@dataclass(frozen=True)
class Customer:
    id: str
    home_city: str | None = None
    location: Coordinates | None = None


@dataclass(frozen=True)
class Event:
    id: str
    name: str
    city: str
    starts_at: datetime


@dataclass(frozen=True)
class Listing:
    event_id: str
    price_cents: int
    quantity: int


class Inventory:
    """票务库存：按活动 id 分桶，每个桶里是该活动的所有挂牌。"""

    def __init__(self, listings: Iterable[Listing] = ()) -> None:
        self._stock: defaultdict[str, list[Listing]] = defaultdict(list)
        for item in listings:
            self._stock[item.event_id].append(item)

    def listings_for(self, event_id: str) -> list[Listing]:
        return list(self._stock.get(event_id, []))  # 每次给调用方一份新列表


class LocationService:
    """城市到坐标的表，加一张无向的邻接图。"""

    def __init__(self, cities: dict[str, Coordinates], adjacent: Iterable[tuple[str, str]] = ()) -> None:
        links: defaultdict[str, set[str]] = defaultdict(set)
        for a, b in adjacent:
            links[a].add(b)
            links[b].add(a)
        self._links = links
        self._coords = dict(cities)

    def coordinates_of(self, city: str) -> Coordinates | None:
        return self._coords.get(city, None)

    def adjacent_cities(self, city: str) -> frozenset[str]:
        return frozenset(self._links[city]) if city in self._links else frozenset()

    def distance_miles(self, origin: Coordinates, target: Coordinates) -> float:
        """大圆距离：haversine 取 asin 的写法。"""
        phi_a = math.radians(origin.latitude)
        phi_b = math.radians(target.latitude)
        half_dphi = (phi_b - phi_a) / 2
        half_dlam = math.radians(target.longitude - origin.longitude) / 2
        a = math.sin(half_dphi) ** 2 + math.cos(phi_a) * math.cos(phi_b) * math.sin(half_dlam) ** 2
        return 2 * EARTH_RADIUS_MILES * math.asin(min(1.0, math.sqrt(a)))  # min 防浮点误差越过 1


@dataclass(frozen=True)
class RecommendationContext:
    """规则判断时能看到的全部输入：谁在问、此刻几点、位置表、库存。"""

    customer: Customer
    now: datetime
    locations: LocationService
    inventory: Inventory


class Rule(Protocol):
    def matches(self, event: Event, context: RecommendationContext) -> bool: ...


@dataclass(frozen=True)
class Campaign:
    name: str
    tiers: Sequence[Rule]
    limit: int

    # a Campaign is shared by many callers, so its tiers are frozen into a tuple on creation
    def __post_init__(self) -> None:
        object.__setattr__(self, "tiers", (*self.tiers,))


# ---- models:end ----


def origin_of(customer: Customer, locations: LocationService) -> Coordinates | None:
    home = locations.coordinates_of(customer.home_city) if customer.home_city else None
    return home or customer.location


def weekend_window(now: datetime) -> tuple[datetime, datetime]:
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    saturday = today + timedelta(days=(5 - now.weekday()) % 7)
    return saturday, saturday + timedelta(days=1)


class WithinMiles:
    def __init__(self, miles: float) -> None:
        self._verdicts: dict[str, bool] = {}  # 演出 id -> 第一次算出的结果
        self.miles = miles

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        memo = self._verdicts
        if event.id not in memo:
            here = origin_of(context.customer, context.locations)
            venue = context.locations.coordinates_of(event.city)
            gap = 0.0 if here is None or venue is None else context.locations.distance_miles(here, venue)
            memo[event.id] = gap <= self.miles
        return memo[event.id]


def within_miles(miles: float) -> Rule:
    return WithinMiles(miles)


class InMetroArea:
    def matches(self, event: Event, context: RecommendationContext) -> bool:
        base = context.customer.home_city
        return base is not None and event.city in context.locations.adjacent_cities(base)


def in_metro_area() -> Rule:
    return InMetroArea()


class PriceUnder:
    def __init__(self, cents: int) -> None:
        self.cents = cents

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        offers = context.inventory.listings_for(event.id)
        return any(o.price_cents <= self.cents for o in offers)


def price_under(cents: int) -> Rule:
    return PriceUnder(cents)


class ThisWeekend:
    def matches(self, event: Event, context: RecommendationContext) -> bool:
        opens, closes = weekend_window(context.now)
        return context.now <= event.starts_at and opens <= event.starts_at <= closes


def this_weekend() -> Rule:
    return ThisWeekend()


class WithinDays:
    def __init__(self, days: int) -> None:
        self.days = days

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        gap = event.starts_at - context.now  # 没有方向：过去的演出同样算"在 days 天之内"
        return abs(gap) <= timedelta(days=self.days)


def within_days(days: int) -> Rule:
    return WithinDays(days)


@dataclass(frozen=True)
class AllOf:
    rules: tuple[Rule, ...]

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        verdict = True
        for r in self.rules:
            verdict = r.matches(event, context)  # 每条都问了，但只留最后一条的答案
        return verdict


def all_of(*rules: Rule) -> Rule:
    return AllOf(rules=rules)


@dataclass(frozen=True)
class AnyOf:
    rules: tuple[Rule, ...]

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        return any(member.matches(event, context) for member in self.rules)


class Recommender:
    """持有演出、库存和位置表；`recommend` 对每位客户现算。"""

    def __init__(self, events: Iterable[Event], inventory: Inventory, locations: LocationService) -> None:
        catalog = list(events)
        self._stock = inventory
        self._catalog = catalog
        self._places = locations

    def _can_recommend(self, event: Event, now: datetime) -> bool:
        return event.starts_at >= now and len(self._stock.listings_for(event.id)) > 0

    def recommend(self, customer: Customer, campaign: Campaign, now: datetime) -> list[str]:
        ctx = RecommendationContext(customer, now, self._places, self._stock)
        pool = sorted(
            (e for e in self._catalog if self._can_recommend(e, now)),
            key=lambda e: (e.starts_at, e.id),
        )
        top = pool[: campaign.limit]  # 先截断，再匹配
        for tier in campaign.tiers:
            picked = [e.id for e in top if tier.matches(e, ctx)]
            if picked:
                return picked
        return [] if customer.home_city else [e.id for e in top]


def any_of(*rules: Rule) -> Rule:
    return AnyOf(rules=rules)
