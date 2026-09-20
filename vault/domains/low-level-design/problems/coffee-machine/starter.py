"""咖啡机（Coffee Machine）——起始模板。

公开的类名、方法签名、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的地方一个个填上，就是一份完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/coffee-machine -q
"""

from __future__ import annotations

import queue
import threading
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime

YUAN = 100


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
        self.missing = dict(missing)


class BrewingFailedError(CoffeeMachineError):
    """冲煮过程中机器出了故障。原料已经原样退回，这一杯不算数。"""


class InvalidQuantityError(CoffeeMachineError):
    """用量或补货量不是正数。"""


@dataclass(frozen=True, slots=True)
class Recipe:
    """一款饮品的配方：名字、价格（分）、每种原料各用多少。不可变。"""

    name: str
    price: int
    ingredients: Mapping[str, int]


def recipe(name: str, price: int, **ingredients: int) -> Recipe:
    """造一份配方：`recipe("拿铁", 22 * YUAN, espresso=30, milk=180)`，用量必须为正。"""
    raise NotImplementedError


@dataclass(frozen=True, slots=True)
class IngredientLow:
    """某种原料刚刚跌到警戒线以下。事件自带余量和警戒线。"""

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
    """所有出口共用的一份原料库存。

    要补全的不变式：余量不为负；扣减全有或全无；余量归零的原料留在表里；同一种原料的
    告警只发一次，直到被补到警戒线以上。
    """

    def __init__(self, levels: Mapping[str, int] | None = None,
                 low_water: Mapping[str, int] | None = None) -> None:
        raise NotImplementedError

    def levels(self) -> Mapping[str, int]:
        """一份只读快照。"""
        raise NotImplementedError

    def low_water_of(self, ingredient: str) -> int:
        raise NotImplementedError

    def set_low_water(self, ingredient: str, mark: int) -> None:
        """设置或修改某种原料的警戒线。"""
        raise NotImplementedError

    def refill(self, ingredient: str, amount: int) -> int:
        """补货，返回补后余量；补到警戒线以上要让告警重新武装。"""
        raise NotImplementedError

    def reserve(self, needs: Mapping[str, int], label: str = "order") -> tuple[IngredientLow, ...]:
        """原子地扣掉一份配方的原料，返回这次新跌破警戒线的原料告警。

        这是整台机器唯一的临界区：算缺口、扣、看谁跌破了线，就这三件事。
        """
        raise NotImplementedError

    def release(self, needs: Mapping[str, int]) -> None:
        """把已经扣掉的原料原样退回。"""
        raise NotImplementedError


Brewer = Callable[[Recipe, str], None]


def instant_brew(drink: Recipe, outlet: str) -> None:
    """默认的"冲煮"：立刻完成。测试要模拟耗时或故障时换掉它。"""
    return None


class CoffeeMachine:
    """一台多出口咖啡机：菜单、共享库存、若干出口，以及告警的发布。

    要补全的不变式：同时冲煮的杯数不超过出口数；一杯要么做出来要么完全没做；任何锁都
    不跨越冲煮；事件一律在锁外投递。
    """

    def __init__(self, inventory: Inventory, recipes: tuple[Recipe, ...] = (), *,
                 outlets: int = 2, brewer: Brewer = instant_brew,
                 clock: Callable[[], datetime] = datetime.now) -> None:
        raise NotImplementedError

    @property
    def inventory(self) -> Inventory:
        raise NotImplementedError

    @property
    def outlet_count(self) -> int:
        raise NotImplementedError

    @property
    def served_count(self) -> int:
        """做成功的杯数。`+= 1` 不是原子操作，它需要自己的锁。"""
        raise NotImplementedError

    def menu(self) -> Mapping[str, Recipe]:
        """一份只读快照。"""
        raise NotImplementedError

    def register(self, drink: Recipe) -> None:
        """加一款新饮品，或用同名配方替换旧的。不检查原料是否已经存在。"""
        raise NotImplementedError

    def subscribe(self, observer: Observer) -> None:
        raise NotImplementedError

    def brew(self, drink: str) -> DrinkServed:
        """做一杯：等出口、扣原料、冲煮，三段各用自己需要的那把锁。"""
        raise NotImplementedError
