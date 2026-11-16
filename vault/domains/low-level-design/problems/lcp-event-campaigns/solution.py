"""活动推荐规则修复（Event Campaigns）：参考解。

设计五行：
1. 规则是只带配置的冻结对象：`matches(event, context)` 的答案只取决于这两个参数，不记任何东西；
2. 一切"这位客户是谁、现在几点、查哪张表"都从 `RecommendationContext` 进来，所以同一个规则对象可以被
   任意多个客户、活动和线程共用；
3. `all_of` / `any_of` 只组合"任何带 `matches` 的对象"，可以嵌套到任意深度，也能装下别处写的规则；
4. 周末窗口用"本周一零点加 5 天、加 7 天"算出，周六日属于当前这一周，周一到周五取的就是即将到来的那一个；
5. `Recommender` 先定出"可推荐集合"（已排序），再逐级匹配：先匹配、后截断，没有一级命中就用同一集合兜底。

下面第一段（models:begin 到 models:end）是工作区里固定的数据类型，复制在这里只为让文件能单独运行；
放进真实工作区时换成 `from models import ...`，其余一字不改。
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import islice
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
    """客户的出发点：分享的精确位置优先；没有才用家所在城市的坐标；都没有就是没有。"""
    if customer.location is not None:
        return customer.location
    if customer.home_city is None:
        return None
    return locations.coordinates_of(customer.home_city)


def weekend_window(now: datetime) -> tuple[datetime, datetime]:
    """`now` 所在周的周末 [周六 00:00, 下周一 00:00)。周一为一周之首，所以周六日算当前这一周。"""
    monday = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now.weekday())
    return monday + timedelta(days=5), monday + timedelta(days=7)


@dataclass(frozen=True, slots=True)
class WithinMiles:
    miles: float

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        origin = origin_of(context.customer, context.locations)
        target = context.locations.coordinates_of(event.city)
        if origin is None or target is None:
            return False  # 缺位置信息是"不匹配"，不是异常，更不是距离 0
        return context.locations.distance_miles(origin, target) <= self.miles


@dataclass(frozen=True, slots=True)
class InMetroArea:
    def matches(self, event: Event, context: RecommendationContext) -> bool:
        home = context.customer.home_city
        if home is None:
            return False
        return event.city == home or event.city in context.locations.adjacent_cities(home)


@dataclass(frozen=True, slots=True)
class PriceUnder:
    cents: int

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        # 同一张票要同时"买得到"且"够便宜"：两个条件落在同一个 listing 上
        return any(
            listing.quantity > 0 and listing.price_cents < self.cents
            for listing in context.inventory.listings_for(event.id)
        )


@dataclass(frozen=True, slots=True)
class ThisWeekend:
    def matches(self, event: Event, context: RecommendationContext) -> bool:
        start, end = weekend_window(context.now)
        return context.now <= event.starts_at and start <= event.starts_at < end


@dataclass(frozen=True, slots=True)
class WithinDays:
    days: int

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        return context.now <= event.starts_at <= context.now + timedelta(days=self.days)


@dataclass(frozen=True, slots=True)
class AllOf:
    rules: tuple[Rule, ...]

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        return all(rule.matches(event, context) for rule in self.rules)


@dataclass(frozen=True, slots=True)
class AnyOf:
    rules: tuple[Rule, ...]

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
    return AllOf(tuple(rules))


def any_of(*rules: Rule) -> Rule:
    return AnyOf(tuple(rules))


class Recommender:
    """唯一持有数据的对象：活动按 (开始时间, id) 排好一次；每次推荐只读它们。"""

    def __init__(self, events: Iterable[Event], inventory: Inventory, locations: LocationService) -> None:
        self._events = tuple(sorted(events, key=lambda event: (event.starts_at, event.id)))
        self._inventory = inventory
        self._locations = locations

    def recommend(self, customer: Customer, campaign: Campaign, now: datetime) -> list[str]:
        context = RecommendationContext(customer, now, self._locations, self._inventory)
        eligible = [event for event in self._events if self._eligible(event, now)]
        for tier in campaign.tiers:
            hits = (event for event in eligible if tier.matches(event, context))
            matched = [event.id for event in islice(hits, campaign.limit)]  # 先匹配，后截断
            if matched:
                return matched  # 第一个有命中的级别决定结果，后面的级别不再看
        return [event.id for event in islice(eligible, campaign.limit)]  # 兜底：人人一样

    def _eligible(self, event: Event, now: datetime) -> bool:
        """还没开始，并且至少有一张买得到的票。"""
        return event.starts_at >= now and any(
            listing.quantity > 0 for listing in self._inventory.listings_for(event.id)
        )


if __name__ == "__main__":
    from datetime import UTC

    places = LocationService(
        {"philadelphia": Coordinates(39.9526, -75.1652), "camden": Coordinates(39.9259, -75.1196)},
        [("philadelphia", "camden")],
    )
    show = Event("e1", "Jazz by the River", "camden", datetime(2026, 11, 8, 20, tzinfo=UTC))
    recommender = Recommender([show], Inventory([Listing("e1", 3500, 12)]), places)
    nearby = any_of(within_miles(100), in_metro_area())
    weekend = Campaign("this-weekend", [all_of(this_weekend(), nearby), all_of(within_days(30), nearby)], 5)
    print(recommender.recommend(Customer("pat", home_city="philadelphia"), weekend, datetime(2026, 11, 5, 9, tzinfo=UTC)))
