"""咖啡机（Coffee Machine）——配方、原料的原子扣减、多出口并发制作与缺料告警。

核心思路：全部难点是一句话——**临界区只有"查库存 + 扣库存"这两步**。冲煮要几十秒，那段
时间一把锁都不持；出口的数量用一个装着出口编号的 `queue.Queue` 表示，等出口和等库存是两件
互不相干的事。库存的扣减是全有或全无：先算出所有缺口，一个都不缺才动手扣，冲煮中途失败则
原样退回，绝不出现"扣了牛奶没扣咖啡"的半杯。缺料告警在锁内**计算**（它要读刚刚变化的库存）、
在锁外**投递**（订阅者可能很慢，甚至会回头调用这台机器）。配方与原料都是数据不是代码：
加一款新饮品、加一种新原料都不需要碰冲煮那条路径。
"""

from __future__ import annotations

import queue
import threading
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType

YUAN = 100  # 价格一律用整数分


class CoffeeMachineError(Exception):
    """本设计全部失败路径的公共基类。"""


class UnknownDrinkError(CoffeeMachineError):
    """菜单上没有这款饮品。"""


class OutOfIngredientError(CoffeeMachineError):
    """原料不够。`missing` 是每种原料还差多少，机器一滴都没有扣。"""

    def __init__(self, drink: str, missing: Mapping[str, int]) -> None:
        detail = "、".join(f"{name} 差 {short}" for name, short in sorted(missing.items()))
        super().__init__(f"cannot brew {drink}: {detail}")
        self.drink = drink
        self.missing = MappingProxyType(dict(missing))


class BrewingFailedError(CoffeeMachineError):
    """冲煮过程中机器出了故障。原料已经原样退回，这一杯不算数。"""


class InvalidQuantityError(CoffeeMachineError):
    """用量或补货量不是正数。"""


@dataclass(frozen=True, slots=True)
class Recipe:
    """一款饮品的配方：名字、价格（分）、每种原料各用多少（毫升或克）。

    不可变。改配方就是注册一个同名的新 `Recipe`，正在冲煮的那一杯不受影响——它手里拿的是
    取菜单那一瞬间的那个对象。
    """

    name: str
    price: int
    ingredients: Mapping[str, int]


def recipe(name: str, price: int, **ingredients: int) -> Recipe:
    """造一份配方：`recipe("拿铁", 22 * YUAN, espresso=30, milk=180)`。

    原料名用关键字参数写出来，配方就是一份数据；用量必须是正整数，0 用量的原料是笔误。
    """
    for material, amount in ingredients.items():
        if amount <= 0:
            raise InvalidQuantityError(f"{name}: {material} must use a positive amount")
    return Recipe(name=name, price=price, ingredients=MappingProxyType(dict(ingredients)))


@dataclass(frozen=True, slots=True)
class IngredientLow:
    """某种原料刚刚跌到警戒线以下。事件自带余量和警戒线，订阅者不必回头读库存。"""

    ingredient: str
    remaining: int
    low_water: int


@dataclass(frozen=True, slots=True)
class DrinkServed:
    """一杯饮品做好了，从哪个出口出的。"""

    drink: str
    outlet: str
    at: datetime


@dataclass(frozen=True, slots=True)
class BrewFailed:
    """冲煮中途失败，原料已退回。"""

    drink: str
    outlet: str
    reason: str
    at: datetime


MachineEvent = IngredientLow | DrinkServed | BrewFailed
Observer = Callable[[MachineEvent], None]


class Inventory:
    """所有出口共用的一份原料库存。它是这道题里唯一真正被并发争用的东西。

    不变式：
    1. 任何原料的余量都不为负——`reserve` 把"查"和"扣"放在同一把锁里做完，中间不给任何
       线程插队的机会。
    2. 扣减是全有或全无：先算出全部缺口，一个都不缺才开始扣。
    3. 余量归零的原料**留在表里**（值为 0），不像钞箱那样删掉——0 和"这台机器根本没有这种
       原料"是两件事，运维要看到前者。
    4. 告警对每种原料只发一次，直到它被补到警戒线以上；`_alerted` 只随原料种类增长。
    """

    def __init__(self, levels: Mapping[str, int] | None = None,
                 low_water: Mapping[str, int] | None = None) -> None:
        self._levels: dict[str, int] = dict(levels or {})
        self._low_water: dict[str, int] = dict(low_water or {})
        self._alerted: set[str] = set()
        self._lock = threading.Lock()  # 故意不是 RLock，见 `CoffeeMachine._publish`

    def levels(self) -> Mapping[str, int]:
        """一份只读快照；库存从不把自己的字典交出去。"""
        with self._lock:
            return MappingProxyType(dict(self._levels))

    def low_water_of(self, ingredient: str) -> int:
        return self._low_water.get(ingredient, 0)

    def set_low_water(self, ingredient: str, mark: int) -> None:
        """设置或修改某种原料的警戒线。"""
        with self._lock:
            self._low_water[ingredient] = mark
            self._relatch(ingredient)

    def refill(self, ingredient: str, amount: int) -> int:
        """补货，返回补后余量。补到警戒线以上会解除告警闩，下次再跌破才会重新告警。"""
        if amount <= 0:
            raise InvalidQuantityError(f"refill amount must be positive, got {amount}")
        with self._lock:
            self._levels[ingredient] = self._levels.get(ingredient, 0) + amount
            self._relatch(ingredient)
            return self._levels[ingredient]

    def reserve(self, needs: Mapping[str, int], label: str = "order") -> tuple[IngredientLow, ...]:
        """原子地扣掉一份配方的原料，返回**这次**新跌破警戒线的原料告警。`label` 只进错误信息。

        这就是整台机器唯一的临界区，而且短得只有三件事：算缺口、扣、看谁跌破了线。冲煮
        不在这里面——把几十秒的冲煮圈进来，N 个出口就退化成 1 个，补货也会被一起卡住。
        告警只在这里**算出来**，投递由调用方在锁外完成。
        """
        with self._lock:
            missing = {name: need - self._levels.get(name, 0)
                       for name, need in needs.items() if self._levels.get(name, 0) < need}
            if missing:
                raise OutOfIngredientError(label, missing)
            events: list[IngredientLow] = []
            for name, need in needs.items():
                self._levels[name] -= need
                mark = self._low_water.get(name, 0)
                if self._levels[name] <= mark and name not in self._alerted:
                    self._alerted.add(name)
                    events.append(IngredientLow(name, self._levels[name], mark))
            return tuple(events)

    def release(self, needs: Mapping[str, int]) -> None:
        """把已经扣掉的原料原样退回——冲煮失败时走这条路，半杯不算数。"""
        with self._lock:
            for name, amount in needs.items():
                self._levels[name] = self._levels.get(name, 0) + amount
                self._relatch(name)

    def _relatch(self, ingredient: str) -> None:
        """余量回到警戒线以上就解除告警闩。必须在锁内调用。"""
        if self._levels.get(ingredient, 0) > self._low_water.get(ingredient, 0):
            self._alerted.discard(ingredient)


# 真实机器里这一步是电机、水泵和加热器；这里注入一个可调用对象，测试可以让它变慢或者失败。
Brewer = Callable[[Recipe, str], None]


def instant_brew(drink: Recipe, outlet: str) -> None:
    """默认的"冲煮"：立刻完成。测试要模拟耗时或故障时换掉它。"""
    return None


class CoffeeMachine:
    """一台多出口咖啡机：菜单、共享库存、若干出口，以及告警的发布。

    不变式：
    1. 同时冲煮的杯数不超过出口数——出口是一个装着出口编号的 `queue.Queue`，取到编号才能
       开始做，做完（无论成败）一定归还。
    2. 一杯要么做出来、要么完全没做：冲煮失败时原料原样退回，`served_count` 不增加。
    3. 任何时刻最多持有一把锁，而且**没有任何一把锁跨越冲煮**。
    4. 事件一律在锁外投递：订阅者可能很慢，甚至会回头调用这台机器。
    """

    def __init__(self, inventory: Inventory, recipes: tuple[Recipe, ...] = (), *,
                 outlets: int = 2, brewer: Brewer = instant_brew,
                 clock: Callable[[], datetime] = datetime.now) -> None:
        if outlets <= 0:
            raise InvalidQuantityError("a machine needs at least one outlet")
        self._inventory = inventory
        self._brewer = brewer
        self._clock = clock
        self._recipes: dict[str, Recipe] = {r.name: r for r in recipes}
        self._menu_lock = threading.Lock()
        self._outlets: queue.Queue[str] = queue.Queue()
        for i in range(outlets):
            self._outlets.put(f"outlet-{i + 1}")
        self._outlet_count = outlets
        self._served = 0
        self._stats_lock = threading.Lock()
        self._observers: list[Observer] = []

    @property
    def inventory(self) -> Inventory:
        """共享库存。它是构造时传进来的协作者，不是这台机器的私有容器——运维直接对它补货，
        机器不需要一个只会转发一行的 `refill()`。"""
        return self._inventory

    @property
    def outlet_count(self) -> int:
        return self._outlet_count

    @property
    def served_count(self) -> int:
        """做成功的杯数。并发测试断言的就是它——`+= 1` 不是原子操作，所以它有自己的锁。"""
        with self._stats_lock:
            return self._served

    def menu(self) -> Mapping[str, Recipe]:
        """一份只读快照。"""
        with self._menu_lock:
            return MappingProxyType(dict(self._recipes))

    def register(self, drink: Recipe) -> None:
        """加一款新饮品，或用同名配方替换旧的（改价、改用量）。

        它不检查原料是否已经存在：新品往往先上菜单、后补原料。真缺料时 `reserve` 会带着
        缺口把它拒掉，而不是抛一个 `KeyError`。
        """
        with self._menu_lock:
            self._recipes[drink.name] = drink

    def subscribe(self, observer: Observer) -> None:
        self._observers.append(observer)

    def brew(self, drink: str) -> DrinkServed:
        """做一杯。等出口、扣原料、冲煮是三段互不重叠的等待，各自只用自己需要的那把锁。"""
        target = self._recipe(drink)
        outlet = self._outlets.get()          # 等一个空闲出口，此时一把锁都没持
        events: list[MachineEvent] = []
        try:
            events.extend(self._inventory.reserve(target.ingredients, label=drink))
            try:
                self._brewer(target, outlet)  # 几十秒的真正工作，不持任何锁
            except Exception as exc:
                self._inventory.release(target.ingredients)
                events.append(BrewFailed(drink, outlet, str(exc), self._clock()))
                raise BrewingFailedError(f"{drink} failed at {outlet}: {exc}") from exc
            with self._stats_lock:
                self._served += 1
            served = DrinkServed(drink, outlet, self._clock())
            events.append(served)
            return served
        finally:
            self._outlets.put(outlet)         # 无论成败，出口一定归还
            self._publish(events)

    def _recipe(self, drink: str) -> Recipe:
        with self._menu_lock:
            target = self._recipes.get(drink)
        if target is None:
            raise UnknownDrinkError(f"no such drink: {drink!r}")
        return target

    def _publish(self, events: list[MachineEvent]) -> None:
        """在**所有**锁之外投递事件。

        这不是讲究：订阅者可能是一个网络调用，也可能回头调用 `machine.inventory.refill(...)`
        （"缺料就自动补货"正是最自然的订阅者）。在库存锁内投递会当场死锁，而把库存锁换成
        `RLock` 只是把死锁换成一个更坏的结果——订阅者在持锁状态下运行，所有出口陪着它等。
        """
        for event in events:
            for observer in self._observers:
                observer(event)


if __name__ == "__main__":
    stock = Inventory({"espresso": 120, "milk": 400, "water": 1000, "cocoa": 40},
                      low_water={"milk": 100, "espresso": 40})
    machine = CoffeeMachine(
        stock,
        (recipe("美式", 18 * YUAN, espresso=30, water=150),
         recipe("拿铁", 22 * YUAN, espresso=30, milk=180)),
        outlets=2)
    machine.subscribe(lambda e: print(f"  [event] {e}"))
    for order in ("拿铁", "拿铁", "美式"):
        print("做好:", machine.brew(order).drink)
    print("库存:", dict(stock.levels()), "共", machine.served_count, "杯")
    try:
        machine.brew("拿铁")
    except OutOfIngredientError as exc:
        print("拒单:", exc)
