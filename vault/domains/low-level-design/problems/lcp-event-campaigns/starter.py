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
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import reduce
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
    """按活动查票。"""

    def __init__(self, listings: Iterable[Listing] = ()) -> None:
        self._by_event: dict[str, list[Listing]] = {}
        for listing in listings:
            self._by_event.setdefault(listing.event_id, []).append(listing)

    def listings_for(self, event_id: str) -> list[Listing]:
        return list(self._by_event.get(event_id, ()))


class LocationService:
    """城市坐标，以及哪些城市两两相邻（双向）。"""

    def __init__(
        self, cities: dict[str, Coordinates], adjacent: Iterable[tuple[str, str]] = ()
    ) -> None:
        self._cities = dict(cities)
        self._adjacent: dict[str, set[str]] = {}
        for first, second in adjacent:
            self._adjacent.setdefault(first, set()).add(second)
            self._adjacent.setdefault(second, set()).add(first)

    def coordinates_of(self, city: str) -> Coordinates | None:
        return self._cities.get(city)

    def adjacent_cities(self, city: str) -> frozenset[str]:
        return frozenset(self._adjacent.get(city, ()))

    def distance_miles(self, origin: Coordinates, target: Coordinates) -> float:
        """球面上两点的大圆距离（haversine 公式）。"""
        lat1, lat2 = math.radians(origin.latitude), math.radians(target.latitude)
        dlon = math.radians(target.longitude - origin.longitude)
        h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        h = min(1.0, max(0.0, h))  # 舍入误差可能让 h 略微越界
        return 2 * EARTH_RADIUS_MILES * math.atan2(math.sqrt(h), math.sqrt(1 - h))


@dataclass(frozen=True)
class RecommendationContext:
    """一条规则可以查看的全部信息：客户、此刻、位置服务、库存。"""

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

    def __post_init__(self) -> None:
        object.__setattr__(self, "tiers", tuple(self.tiers))


# ---- models:end ----

def origin_of(customer: Customer, locations: LocationService) -> Coordinates | None:
    if customer.home_city is not None:
        home = locations.coordinates_of(customer.home_city)
        if home is not None:
            return home
    return customer.location


def weekend_window(now: datetime) -> tuple[datetime, datetime]:
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    saturday = midnight + timedelta(days=(5 - now.weekday()) % 7)
    return saturday, saturday + timedelta(days=1)


class WithinMiles:
    def __init__(self, miles: float) -> None:
        self.miles = miles
        self._seen: dict[str, float] = {}  # 活动城市 -> 距离，省得重复计算

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        if event.city not in self._seen:
            origin = origin_of(context.customer, context.locations)
            target = context.locations.coordinates_of(event.city)
            if origin is None or target is None:
                self._seen[event.city] = 0.0
            else:
                self._seen[event.city] = context.locations.distance_miles(origin, target)
        return self._seen[event.city] <= self.miles


class InMetroArea:
    def matches(self, event: Event, context: RecommendationContext) -> bool:
        home = context.customer.home_city
        return home is not None and event.city in context.locations.adjacent_cities(home)


class PriceUnder:
    def __init__(self, cents: int) -> None:
        self.cents = cents

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        prices = [listing.price_cents for listing in context.inventory.listings_for(event.id)]
        return bool(prices) and min(prices) <= self.cents


class ThisWeekend:
    def matches(self, event: Event, context: RecommendationContext) -> bool:
        start, end = weekend_window(context.now)
        return context.now <= event.starts_at and start <= event.starts_at <= end


class WithinDays:
    def __init__(self, days: int) -> None:
        self.days = days

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        return abs(event.starts_at - context.now) <= timedelta(days=self.days)


class AllOf:
    def __init__(self, rules: Iterable[Rule]) -> None:
        self.rules = tuple(rules)

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        return reduce(lambda _, rule: rule.matches(event, context), self.rules, True)


class AnyOf:
    def __init__(self, rules: Iterable[Rule]) -> None:
        self.rules = tuple(rules)

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        return any(rule.matches(event, context) for rule in self.rules)


def within_miles(miles: float) -> Rule:
    return WithinMiles(miles)


def in_metro_area() -> Rule:
    return InMetroArea()


def price_under(cents: int) -> Rule:
    return PriceUnder(cents)


def this_weekend() -> Rule:
    return ThisWeekend()


def within_days(days: int) -> Rule:
    return WithinDays(days)


def all_of(*rules: Rule) -> Rule:
    return AllOf(rules)


def any_of(*rules: Rule) -> Rule:
    return AnyOf(rules)


class Recommender:
    def __init__(self, events: Iterable[Event], inventory: Inventory, locations: LocationService) -> None:
        self._events = list(events)
        self._inventory = inventory
        self._locations = locations

    def recommend(self, customer: Customer, campaign: Campaign, now: datetime) -> list[str]:
        context = RecommendationContext(customer, now, self._locations, self._inventory)
        eligible = sorted(
            (event for event in self._events if self._eligible(event, now)),
            key=lambda event: (event.starts_at, event.id),
        )
        shortlist = eligible[: campaign.limit]  # 先截断，再匹配
        for tier in campaign.tiers:
            matched = [event.id for event in shortlist if tier.matches(event, context)]
            if matched:
                return matched
        return [] if customer.home_city else [event.id for event in shortlist]

    def _eligible(self, event: Event, now: datetime) -> bool:
        return event.starts_at >= now and bool(self._inventory.listings_for(event.id))
