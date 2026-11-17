"""活动推荐规则修复（Event Campaigns）：参考解。

设计五行：
1. 规则是只带配置的冻结对象：`matches(event, context)` 的答案只取决于这两个参数，自己不记任何东西；
2. "这位客户是谁、现在几点、查哪张表"全部经由 `RecommendationContext` 传入，所以一个规则对象
   可以被任意多个客户、活动和线程共用；
3. `all_of` / `any_of` 只要求成员有 `matches` 方法，因此能嵌套到任意深度，也能装下别处写的规则；
4. 周末窗口用"本周一零点 + 5 天 / + 7 天"得到：周六日落在当前这一周，周一到周五则指向即将到来的周末；
5. `Recommender` 先得到排好序的"可推荐集合"，再逐级匹配：先匹配、后截断；没有一级命中就返回这个集合的开头。

models:begin 到 models:end 之间是工作区里固定不动的数据类型，这里写了一份自己的实现，只为让本文件能单独运行；
放进真实工作区时把这一段换成 `from models import ...`，其余部分原样使用。
"""

from __future__ import annotations

import math
from collections import defaultdict
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
    """出发点：精确位置第一；其次是位置表认识的家乡城市；两样都没有就返回 None。"""
    if customer.location is not None:
        return customer.location
    if customer.home_city is None:
        return None
    return locations.coordinates_of(customer.home_city)


def weekend_window(now: datetime) -> tuple[datetime, datetime]:
    """半开区间 [周六 00:00, 下周一 00:00)。以周一为一周之首，周六日就属于 `now` 所在的这一周。"""
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    monday = today - timedelta(days=now.weekday())
    return monday + timedelta(days=5), monday + timedelta(days=7)


@dataclass(frozen=True, slots=True)
class WithinMiles:
    miles: float

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        here = origin_of(context.customer, context.locations)
        venue = context.locations.coordinates_of(event.city)
        if here is None or venue is None:
            return False  # 不知道在哪里，就不能说"在范围内"；它既不是异常，也不是 0 英里
        return context.locations.distance_miles(here, venue) <= self.miles


def within_miles(miles: float) -> Rule:
    return WithinMiles(miles=miles)


@dataclass(frozen=True, slots=True)
class InMetroArea:
    def matches(self, event: Event, context: RecommendationContext) -> bool:
        base = context.customer.home_city
        # 家本身算，直接相邻的城市算；没有家，就没有都市圈
        return base is not None and event.city in {base, *context.locations.adjacent_cities(base)}


def in_metro_area() -> Rule:
    return InMetroArea()


@dataclass(frozen=True, slots=True)
class PriceUnder:
    cents: int

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        # 买得到和够便宜要由同一张票同时满足
        offers = context.inventory.listings_for(event.id)
        return any(o.quantity > 0 and o.price_cents < self.cents for o in offers)


def price_under(cents: int) -> Rule:
    return PriceUnder(cents=cents)


@dataclass(frozen=True, slots=True)
class ThisWeekend:
    def matches(self, event: Event, context: RecommendationContext) -> bool:
        opens, closes = weekend_window(context.now)
        return max(context.now, opens) <= event.starts_at < closes


def this_weekend() -> Rule:
    return ThisWeekend()


@dataclass(frozen=True, slots=True)
class WithinDays:
    days: int

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        horizon = context.now + timedelta(days=self.days)
        return context.now <= event.starts_at <= horizon


def within_days(days: int) -> Rule:
    return WithinDays(days=days)


@dataclass(frozen=True, slots=True)
class AllOf:
    rules: tuple[Rule, ...]

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        return all(r.matches(event, context) for r in self.rules)


def all_of(*rules: Rule) -> Rule:
    return AllOf(rules=rules)


@dataclass(frozen=True, slots=True)
class AnyOf:
    rules: tuple[Rule, ...]

    def matches(self, event: Event, context: RecommendationContext) -> bool:
        return any(r.matches(event, context) for r in self.rules)


def any_of(*rules: Rule) -> Rule:
    return AnyOf(rules=rules)


class Recommender:
    """唯一持有数据的对象：活动在构造时按 (开始时间, id) 排好，之后每次推荐都只读。"""

    def __init__(self, events: Iterable[Event], inventory: Inventory, locations: LocationService) -> None:
        by_start = sorted(events, key=lambda e: (e.starts_at, e.id))
        self._events = tuple(by_start)
        self._stock = inventory
        self._places = locations

    def _can_recommend(self, event: Event, now: datetime) -> bool:
        """没开始，并且至少还有一张能买的票。"""
        if event.starts_at < now:
            return False
        return any(o.quantity > 0 for o in self._stock.listings_for(event.id))

    def recommend(self, customer: Customer, campaign: Campaign, now: datetime) -> list[str]:
        ctx = RecommendationContext(customer, now, self._places, self._stock)
        pool = [e for e in self._events if self._can_recommend(e, now)]
        for tier in campaign.tiers:
            hits = (e for e in pool if tier.matches(e, ctx))
            picked = [e.id for e in islice(hits, campaign.limit)]  # 先匹配，再截断
            if picked:
                return picked  # 第一个有命中的级别说了算
        return [e.id for e in pool[: campaign.limit]]  # 没有级别命中：每位客户拿到同样的开头


if __name__ == "__main__":
    from datetime import UTC

    places = LocationService(
        {"seattle": Coordinates(47.6062, -122.3321), "bellevue": Coordinates(47.6101, -122.2015)},
        [("seattle", "bellevue")],
    )
    concert = Event("c1", "Harbor Lights Concert", "bellevue", datetime(2026, 11, 8, 20, tzinfo=UTC))
    recommender = Recommender([concert], Inventory([Listing("c1", 4200, 8)]), places)
    close = any_of(within_miles(25), in_metro_area())
    campaign = Campaign("weekend-picks", [all_of(this_weekend(), close), all_of(within_days(14), close)], 3)
    print(recommender.recommend(Customer("pat", home_city="seattle"), campaign, datetime(2026, 11, 5, 9, tzinfo=UTC)))
