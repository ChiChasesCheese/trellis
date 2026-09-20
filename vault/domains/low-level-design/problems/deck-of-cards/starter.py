"""扑克牌与二十一点（Deck of Cards / Blackjack）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass`、类型别名、取值表和异常都和 `solution.py` 一致；
把标了 `raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/deck-of-cards -q
"""

from __future__ import annotations

import random
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType


class CardGameError(Exception):
    """本设计里所有失败路径的公共基类。"""


class OutOfCardsError(CardGameError):
    """牌不够发了。"""


class UnsupportedCardError(CardGameError):
    """这个游戏不认识这张牌（比如 21 点遇到小丑牌）。"""


class GameStateError(CardGameError):
    """在不该调用的时候调用了。"""


class Suit(Enum):
    """花色。`STARS` 是第 4 关的第五门花色，标准 52 张牌里不含它。"""

    CLUBS = ("♣", 0)
    DIAMONDS = ("♦", 1)
    HEARTS = ("♥", 2)
    SPADES = ("♠", 3)
    STARS = ("★", 4)

    def __init__(self, symbol: str, order: int) -> None:
        self.symbol = symbol
        self.order = order


class Rank(Enum):
    """点数。`order` 是印在牌上的自然顺序，不是任何一个游戏里的大小或分值。"""

    ACE = ("A", 1)
    TWO = ("2", 2)
    THREE = ("3", 3)
    FOUR = ("4", 4)
    FIVE = ("5", 5)
    SIX = ("6", 6)
    SEVEN = ("7", 7)
    EIGHT = ("8", 8)
    NINE = ("9", 9)
    TEN = ("10", 10)
    JACK = ("J", 11)
    QUEEN = ("Q", 12)
    KING = ("K", 13)
    JOKER = ("Jk", 0)

    def __init__(self, label: str, order: int) -> None:
        self.label = label
        self.order = order


@dataclass(frozen=True, slots=True)
class Card:
    """一张牌：不可变、可哈希、可排序、`__repr__` 一眼能读懂，身上没有任何游戏规则。"""

    rank: Rank
    suit: Suit

    @property
    def sort_key(self) -> tuple[int, int]:
        """默认排序依据：按牌面自然顺序，同点数再按花色。"""
        raise NotImplementedError

    def __lt__(self, other: Card) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


STANDARD_RANKS: tuple[Rank, ...] = tuple(r for r in Rank if r is not Rank.JOKER)
STANDARD_SUITS: tuple[Suit, ...] = (Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES)


def build_deck(
    copies: int = 1,
    *,
    ranks: Sequence[Rank] = STANDARD_RANKS,
    suits: Sequence[Suit] = STANDARD_SUITS,
    jokers: int = 0,
) -> tuple[Card, ...]:
    """按给定的点数／花色清单造牌——注意遍历传进来的清单，而不是 `for s in Suit`。"""
    raise NotImplementedError


class Deck:
    """一摞牌，顶在末尾。牌只能通过 `deal` 离开、通过 `place_at_bottom` 回来。"""

    def __init__(self, cards: Iterable[Card] = ()) -> None:
        raise NotImplementedError

    @property
    def remaining(self) -> int:
        """还剩几张——外界能知道的关于牌堆内容的全部。"""
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def shuffle(self, rng: random.Random) -> None:
        """洗牌，随机源必填。"""
        raise NotImplementedError

    def deal(self, count: int = 1) -> tuple[Card, ...]:
        """从顶上发 `count` 张；牌不够抛 `OutOfCardsError`，绝不少发。"""
        raise NotImplementedError

    def deal_one(self) -> Card:
        """发一张。"""
        raise NotImplementedError

    def place_at_bottom(self, cards: Iterable[Card]) -> None:
        """把牌放回底部。"""
        raise NotImplementedError


class ShoeEventKind(Enum):
    """牌鞋发生的两件事。"""

    DEALT = "dealt"
    SHUFFLED = "shuffled"


@dataclass(frozen=True, slots=True)
class ShoeEvent:
    """牌鞋推给订阅者的事件：事件自带发生了什么。"""

    kind: ShoeEventKind
    cards: tuple[Card, ...]
    remaining: int
    decks_remaining: float


class Shoe:
    """赌场牌鞋：几副牌摞在一起，插一张切牌，切到就该重洗。"""

    def __init__(
        self,
        decks: int = 6,
        *,
        rng: random.Random,
        penetration: float = 0.75,
        builder: Callable[[], tuple[Card, ...]] = build_deck,
    ) -> None:
        raise NotImplementedError

    @property
    def remaining(self) -> int:
        """还剩几张。"""
        raise NotImplementedError

    @property
    def decks_remaining(self) -> float:
        """还剩几副。"""
        raise NotImplementedError

    @property
    def needs_shuffle(self) -> bool:
        """切牌标记到了没有；到了也不会自动洗。"""
        raise NotImplementedError

    def shuffle(self) -> None:
        """重新装满并洗牌，然后广播 SHUFFLED 事件。"""
        raise NotImplementedError

    def deal(self, count: int = 1) -> tuple[Card, ...]:
        """发牌并广播 DEALT 事件。"""
        raise NotImplementedError

    def subscribe(self, listener: Callable[[ShoeEvent], None]) -> Callable[[], None]:
        """订阅事件，返回取消订阅的函数。"""
        raise NotImplementedError


HI_LO: Mapping[Rank, int] = MappingProxyType(
    {
        Rank.TWO: 1, Rank.THREE: 1, Rank.FOUR: 1, Rank.FIVE: 1, Rank.SIX: 1,
        Rank.SEVEN: 0, Rank.EIGHT: 0, Rank.NINE: 0,
        Rank.TEN: -1, Rank.JACK: -1, Rank.QUEEN: -1, Rank.KING: -1, Rank.ACE: -1,
    }
)


class RunningCount:
    """算牌器：一个纯粹的观察者，只从事件里取数据。"""

    def __init__(self, shoe: Shoe, counts: Mapping[Rank, int] = HI_LO) -> None:
        raise NotImplementedError

    @property
    def running(self) -> int:
        """跑动计数。"""
        raise NotImplementedError

    @property
    def true_count(self) -> float:
        """真数＝跑动计数 ÷ 剩余副数。"""
        raise NotImplementedError

    def detach(self) -> None:
        """不再算了。"""
        raise NotImplementedError


BLACKJACK_VALUES: Mapping[Rank, int] = MappingProxyType(
    {
        Rank.ACE: 1, Rank.TWO: 2, Rank.THREE: 3, Rank.FOUR: 4, Rank.FIVE: 5,
        Rank.SIX: 6, Rank.SEVEN: 7, Rank.EIGHT: 8, Rank.NINE: 9, Rank.TEN: 10,
        Rank.JACK: 10, Rank.QUEEN: 10, Rank.KING: 10,
    }
)


class Outcome(Enum):
    """一局 21 点的四种结局。"""

    PLAYER_BLACKJACK = "player_blackjack"
    PLAYER_WIN = "player_win"
    DEALER_WIN = "dealer_win"
    PUSH = "push"


class BlackjackHand:
    """一手 21 点的牌：它拥有"这手牌值几点"这条规则，而 `Card` 不拥有。"""

    def __init__(self, cards: Iterable[Card] = ()) -> None:
        raise NotImplementedError

    @property
    def cards(self) -> tuple[Card, ...]:
        """手牌快照。"""
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def add(self, *cards: Card) -> None:
        """要牌；取值表里没有的牌当场抛 `UnsupportedCardError`。"""
        raise NotImplementedError

    @property
    def total(self) -> int:
        """点数：A 先按 1 算，若再加 10 不爆就让其中一张 A 当 11。"""
        raise NotImplementedError

    @property
    def is_soft(self) -> bool:
        """软牌：有一张 A 正被当成 11。"""
        raise NotImplementedError

    @property
    def is_bust(self) -> bool:
        """爆牌。"""
        raise NotImplementedError

    @property
    def is_blackjack(self) -> bool:
        """恰好两张牌凑成 21。"""
        raise NotImplementedError


HitPolicy = Callable[[BlackjackHand], bool]


def stand_on_17(hand: BlackjackHand) -> bool:
    """庄家标准策略：17 点及以上停牌。"""
    raise NotImplementedError


def hit_soft_17(hand: BlackjackHand) -> bool:
    """庄家另一种常见策略：软 17 还要一张。"""
    raise NotImplementedError


def stand_on(threshold: int) -> HitPolicy:
    """玩家策略工厂：到 `threshold` 点就停。"""
    raise NotImplementedError


@dataclass(frozen=True, slots=True)
class RoundResult:
    """一局 21 点的结果，纯数据。"""

    player: tuple[Card, ...]
    dealer: tuple[Card, ...]
    player_total: int
    dealer_total: int
    outcome: Outcome


class BlackjackGame:
    """21 点：从牌鞋要牌，但对牌鞋里是几副、有没有小丑牌一无所知。"""

    def __init__(self, shoe: Shoe, *, dealer_policy: HitPolicy = stand_on_17) -> None:
        raise NotImplementedError

    def play_round(self, player_policy: HitPolicy = stand_on_17) -> RoundResult:
        """打一局：发两张、玩家按策略要牌、庄家按策略要牌、比点数。"""
        raise NotImplementedError


def war_order(card: Card) -> int:
    """战争里 A 最大——同一张牌在两个游戏里有不同的序。"""
    raise NotImplementedError


@dataclass(frozen=True, slots=True)
class WarRound:
    """一个回合：双方亮的牌、谁赢、这回合押上了多少张。"""

    revealed: tuple[Card, ...]
    winner: int | None
    pot_size: int


class WarGame:
    """战争：用和 21 点完全相同的 `Card` 与 `Deck`。"""

    def __init__(self, deck: Deck) -> None:
        raise NotImplementedError

    @property
    def pile_sizes(self) -> tuple[int, int]:
        """两摞牌各剩几张。"""
        raise NotImplementedError

    def play_round(self) -> WarRound:
        """打一个回合；押上去的牌一定会回到某个人手里，牌的总数守恒。"""
        raise NotImplementedError

    def play(self, max_rounds: int = 2000) -> int | None:
        """一直打到一方收光或回合数耗尽。"""
        raise NotImplementedError
