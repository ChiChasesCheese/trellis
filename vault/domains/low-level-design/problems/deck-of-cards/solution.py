"""扑克牌与二十一点（Deck of Cards / Blackjack）——通用牌组抽象，游戏规则长在游戏那一侧。

核心思路：`Card` 是不可变值对象（可哈希、可排序、`__repr__` 人能读），身上**没有任何游戏
规则**——同一张 A 在 21 点里算 11 或 1、在战争（War）里最大、在别的玩法里又是别的，一个属性
不可能同时正确，所以取值是游戏自己的一张表。`Deck` 只暴露"还剩几张"和"发牌"，内部那份牌列表
永远不交出去；洗牌的随机源必须注入。`Shoe` 把若干副牌摞在一起并管切牌标记，它只向订阅者
**推事件**、不知道有人在算牌；`RunningCount` 完全靠事件更新自己。加小丑牌或者第五门花色改的
是牌堆的**组成**（显式的花色／点数清单），不是枚举也不是游戏。
"""

from __future__ import annotations

import random
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType

# --------------------------------------------------------------------------
# 失败路径


class CardGameError(Exception):
    """本设计里所有失败路径的公共基类。"""


class OutOfCardsError(CardGameError):
    """牌不够发了——空牌堆继续发牌是这道题必须点名的失败路径。"""


class UnsupportedCardError(CardGameError):
    """这个游戏不认识这张牌（比如 21 点遇到小丑牌）：大声报错，而不是悄悄按 0 分算。"""


class GameStateError(CardGameError):
    """在不该调用的时候调用了（比如一局还没发牌就结算）。"""


# --------------------------------------------------------------------------
# 牌：不可变值对象，身上不带任何游戏规则


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
    """点数。`order` 是**印在牌上的自然顺序**（A 排第一），不是任何一个游戏里的大小或分值。"""

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
    """一张牌：不可变、可哈希（能进 `set` 和字典）、可排序、`__repr__` 一眼能读懂。

    它**不知道**自己在 21 点里值几分、在战争里大不大——那些是游戏的知识。
    """

    rank: Rank
    suit: Suit

    @property
    def sort_key(self) -> tuple[int, int]:
        """默认的排序依据：按牌面的自然顺序，同点数再按花色。"""
        return (self.rank.order, self.suit.order)

    def __lt__(self, other: Card) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.sort_key < other.sort_key

    def __repr__(self) -> str:
        return f"{self.rank.label}{self.suit.symbol}"


STANDARD_RANKS: tuple[Rank, ...] = tuple(r for r in Rank if r is not Rank.JOKER)
STANDARD_SUITS: tuple[Suit, ...] = (Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES)


def build_deck(
    copies: int = 1,
    *,
    ranks: Sequence[Rank] = STANDARD_RANKS,
    suits: Sequence[Suit] = STANDARD_SUITS,
    jokers: int = 0,
) -> tuple[Card, ...]:
    """按给定的点数／花色清单造牌。

    注意它遍历的是**显式传进来的清单**而不是 `for s in Suit`：枚举是封闭集合，而"这副牌由
    哪些牌组成"是开放的。第 4 关加小丑牌或第五门花色，改的正是这两个参数。
    """
    if copies < 1:
        raise CardGameError(f"至少要一副牌，给的是 {copies}")
    if not 0 <= jokers <= 2:
        raise CardGameError(f"每副牌最多两张小丑牌，给的是 {jokers}")
    cards: list[Card] = []
    for _ in range(copies):
        cards.extend(Card(rank, suit) for suit in suits for rank in ranks)
        cards.extend(Card(Rank.JOKER, s) for s in (Suit.SPADES, Suit.HEARTS)[:jokers])
    return tuple(cards)


# --------------------------------------------------------------------------
# 牌堆：只说"还剩几张"，永远不把牌列表交出去


class Deck:
    """一摞牌，顶在列表末尾。

    它拥有的不变量只有一条：**牌只能通过 `deal` 离开、通过 `place_at_bottom` 回来**。
    所以这里没有 `cards` 属性，也没有 `get_cards()`——交出内部列表等于交出洗牌、偷看、
    删牌的权力，`Deck` 就不再是牌堆，只是一个带方法的 list。
    """

    def __init__(self, cards: Iterable[Card] = ()) -> None:
        self._cards: list[Card] = list(cards)

    @property
    def remaining(self) -> int:
        """还剩几张。这是外界能知道的关于牌堆内容的**全部**。"""
        return len(self._cards)

    def __len__(self) -> int:
        return len(self._cards)

    def shuffle(self, rng: random.Random) -> None:
        """洗牌。随机源是**必填参数**：一个默认用全局 `random` 的洗牌方法，会让所有下游测试失去可复现性。"""
        rng.shuffle(self._cards)

    def deal(self, count: int = 1) -> tuple[Card, ...]:
        """从顶上发 `count` 张，按发牌顺序返回。牌不够就抛 `OutOfCardsError`，绝不少发。"""
        if count < 1:
            raise CardGameError(f"一次至少发一张，给的是 {count}")
        if count > len(self._cards):
            raise OutOfCardsError(f"牌堆只剩 {len(self._cards)} 张，发不出 {count} 张")
        dealt = tuple(reversed(self._cards[-count:]))
        del self._cards[-count:]
        return dealt

    def deal_one(self) -> Card:
        """发一张。"""
        return self.deal(1)[0]

    def place_at_bottom(self, cards: Iterable[Card]) -> None:
        """把牌放回底部——战争、斗地主这类"赢来的牌压到底下"的玩法需要它。"""
        self._cards[:0] = list(cards)


# --------------------------------------------------------------------------
# 牌鞋：若干副牌 + 切牌标记 + 事件


class ShoeEventKind(Enum):
    """牌鞋发生的两件事。"""

    DEALT = "dealt"
    SHUFFLED = "shuffled"


@dataclass(frozen=True, slots=True)
class ShoeEvent:
    """牌鞋推给订阅者的事件：**事件自带发生了什么**，订阅者不需要回头去问牌鞋。"""

    kind: ShoeEventKind
    cards: tuple[Card, ...]
    remaining: int
    decks_remaining: float


class Shoe:
    """赌场里的牌鞋：几副牌摞在一起，插一张切牌（cut card），切到就该重洗。

    它不知道 21 点，也不知道有人在算牌；它只管发牌和在恰当的时候说"该洗了"。
    """

    def __init__(
        self,
        decks: int = 6,
        *,
        rng: random.Random,
        penetration: float = 0.75,
        builder: Callable[[], tuple[Card, ...]] = build_deck,
    ) -> None:
        if decks < 1:
            raise CardGameError(f"牌鞋里至少要一副牌，给的是 {decks}")
        if not 0 < penetration < 1:
            raise CardGameError(f"穿透率要在 0 和 1 之间，给的是 {penetration}")
        self._decks = decks
        self._rng = rng
        self._builder = builder
        self._cards_per_deck = len(builder())
        self._cut_at = round(self._cards_per_deck * decks * (1 - penetration))
        self._listeners: list[Callable[[ShoeEvent], None]] = []
        self._deck = Deck()
        self.shuffle()

    @property
    def remaining(self) -> int:
        """还剩几张。"""
        return self._deck.remaining

    @property
    def decks_remaining(self) -> float:
        """还剩几副——算牌把跑动计数换算成真数（true count）时要用它。"""
        return self._deck.remaining / self._cards_per_deck

    @property
    def needs_shuffle(self) -> bool:
        """切牌标记到了没有。到了也**不会自动洗**：一局牌要打完再洗，洗牌是调用方的决定。"""
        return self._deck.remaining <= self._cut_at

    def shuffle(self) -> None:
        """重新装满并洗牌，然后广播一个 SHUFFLED 事件——算牌器靠它把计数归零。"""
        self._deck = Deck(card for _ in range(self._decks) for card in self._builder())
        self._deck.shuffle(self._rng)
        self._emit(ShoeEventKind.SHUFFLED, ())

    def deal(self, count: int = 1) -> tuple[Card, ...]:
        """发牌并广播 DEALT 事件。"""
        cards = self._deck.deal(count)
        self._emit(ShoeEventKind.DEALT, cards)
        return cards

    def subscribe(self, listener: Callable[[ShoeEvent], None]) -> Callable[[], None]:
        """订阅事件，返回取消订阅的函数——监听器表因此不会只进不出。"""
        self._listeners.append(listener)

        def unsubscribe() -> None:
            if listener in self._listeners:
                self._listeners.remove(listener)

        return unsubscribe

    def _emit(self, kind: ShoeEventKind, cards: tuple[Card, ...]) -> None:
        event = ShoeEvent(kind, cards, self._deck.remaining, self.decks_remaining)
        for listener in tuple(self._listeners):
            listener(event)


HI_LO: Mapping[Rank, int] = MappingProxyType(
    {
        Rank.TWO: 1, Rank.THREE: 1, Rank.FOUR: 1, Rank.FIVE: 1, Rank.SIX: 1,
        Rank.SEVEN: 0, Rank.EIGHT: 0, Rank.NINE: 0,
        Rank.TEN: -1, Rank.JACK: -1, Rank.QUEEN: -1, Rank.KING: -1, Rank.ACE: -1,
    }
)


class RunningCount:
    """算牌器：一个纯粹的观察者。牌鞋完全不知道它存在，去掉它牌鞋的行为一模一样。

    它只从事件里取数据——发了哪几张、还剩几副——从不反过来读牌鞋的内部状态。
    """

    def __init__(self, shoe: Shoe, counts: Mapping[Rank, int] = HI_LO) -> None:
        self._counts = counts
        self._running = 0
        self._decks_remaining = shoe.decks_remaining
        self._detach = shoe.subscribe(self._on_event)

    @property
    def running(self) -> int:
        """跑动计数（running count）：小牌 +1、大牌 -1 的累计。"""
        return self._running

    @property
    def true_count(self) -> float:
        """真数（true count）＝跑动计数 ÷ 剩余副数。剩不到四分之一副时不再有意义，返回跑动计数本身。"""
        return self._running / self._decks_remaining if self._decks_remaining >= 0.25 else float(self._running)

    def detach(self) -> None:
        """不再算了。"""
        self._detach()

    def _on_event(self, event: ShoeEvent) -> None:
        if event.kind is ShoeEventKind.SHUFFLED:
            self._running = 0
        else:
            self._running += sum(self._counts.get(c.rank, 0) for c in event.cards)
        self._decks_remaining = event.decks_remaining


# --------------------------------------------------------------------------
# 游戏一：二十一点。规则全在这一段，上面那些类一个字都不知道 21 点

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
    """一手 21 点的牌。它拥有"这手牌值几点"这条规则，而 `Card` 不拥有。"""

    def __init__(self, cards: Iterable[Card] = ()) -> None:
        self._cards: list[Card] = []
        self.add(*cards)

    @property
    def cards(self) -> tuple[Card, ...]:
        """手牌快照。手牌对持有者是公开信息，和牌堆不同——但交出去的仍然是快照。"""
        return tuple(self._cards)

    def __len__(self) -> int:
        return len(self._cards)

    def add(self, *cards: Card) -> None:
        """要牌。遇到取值表里没有的牌（小丑牌）当场抛错，而不是按 0 分算。"""
        for card in cards:
            if card.rank not in BLACKJACK_VALUES:
                raise UnsupportedCardError(f"21 点不认识 {card!r}；要支持它，往取值表里加一条")
            self._cards.append(card)

    @property
    def total(self) -> int:
        """点数。A 先按 1 算，若有 A 且再加 10 不爆，就让**其中一张** A 当 11。"""
        hard = sum(BLACKJACK_VALUES[c.rank] for c in self._cards)
        if self._has_ace and hard + 10 <= 21:
            return hard + 10
        return hard

    @property
    def is_soft(self) -> bool:
        """软牌：有一张 A 正被当成 11。软 17 该不该继续要牌，是庄家策略的分水岭。"""
        hard = sum(BLACKJACK_VALUES[c.rank] for c in self._cards)
        return self._has_ace and hard + 10 <= 21

    @property
    def is_bust(self) -> bool:
        """爆牌。"""
        return self.total > 21

    @property
    def is_blackjack(self) -> bool:
        """黑杰克：**恰好两张**牌凑成 21；三张 7 是 21 但不是黑杰克。"""
        return len(self._cards) == 2 and self.total == 21

    @property
    def _has_ace(self) -> bool:
        return any(c.rank is Rank.ACE for c in self._cards)

    def __repr__(self) -> str:
        return f"BlackjackHand({' '.join(repr(c) for c in self._cards)}={self.total})"


HitPolicy = Callable[[BlackjackHand], bool]


def stand_on_17(hand: BlackjackHand) -> bool:
    """庄家标准策略：17 点及以上停牌。"""
    return hand.total < 17


def hit_soft_17(hand: BlackjackHand) -> bool:
    """庄家另一种常见策略：软 17 还要一张。换策略只是换一个函数。"""
    return hand.total < 17 or (hand.total == 17 and hand.is_soft)


def stand_on(threshold: int) -> HitPolicy:
    """玩家策略工厂：到 `threshold` 点就停。"""
    return lambda hand: hand.total < threshold


@dataclass(frozen=True, slots=True)
class RoundResult:
    """一局 21 点的结果，纯数据——渲染、统计、下注模块都从它取数。"""

    player: tuple[Card, ...]
    dealer: tuple[Card, ...]
    player_total: int
    dealer_total: int
    outcome: Outcome


class BlackjackGame:
    """21 点。它从牌鞋里要牌，但对牌鞋里是几副、有没有小丑牌、花色有几门一无所知。"""

    def __init__(self, shoe: Shoe, *, dealer_policy: HitPolicy = stand_on_17) -> None:
        self._shoe = shoe
        self._dealer_policy = dealer_policy

    def play_round(self, player_policy: HitPolicy = stand_on_17) -> RoundResult:
        """打一局：发两张、玩家按策略要牌、庄家按策略要牌、比点数。"""
        if self._shoe.remaining < 4:
            raise GameStateError("牌鞋里的牌不够开一局了，先洗牌")
        player = BlackjackHand(self._shoe.deal(2))
        dealer = BlackjackHand(self._shoe.deal(2))
        if player.is_blackjack or dealer.is_blackjack:
            return self._settle(player, dealer)
        while player_policy(player) and not player.is_bust:
            player.add(*self._shoe.deal(1))
        if not player.is_bust:
            while self._dealer_policy(dealer) and not dealer.is_bust:
                dealer.add(*self._shoe.deal(1))
        return self._settle(player, dealer)

    def _settle(self, player: BlackjackHand, dealer: BlackjackHand) -> RoundResult:
        """结算顺序是有讲究的：先判黑杰克，再判爆牌，最后才比点数。"""
        if player.is_blackjack or dealer.is_blackjack:
            if player.is_blackjack and dealer.is_blackjack:
                outcome = Outcome.PUSH
            else:
                outcome = Outcome.PLAYER_BLACKJACK if player.is_blackjack else Outcome.DEALER_WIN
        elif player.is_bust:
            outcome = Outcome.DEALER_WIN
        elif dealer.is_bust or player.total > dealer.total:
            outcome = Outcome.PLAYER_WIN
        elif player.total < dealer.total:
            outcome = Outcome.DEALER_WIN
        else:
            outcome = Outcome.PUSH
        return RoundResult(player.cards, dealer.cards, player.total, dealer.total, outcome)


# --------------------------------------------------------------------------
# 游戏二：战争（War）。同一副 Deck，另一套规则——这才是抽象成立的证据


def war_order(card: Card) -> int:
    """战争里 A 最大。**同一张牌在两个游戏里有不同的序**，所以序不能长在 `Card` 上。"""
    return 14 if card.rank is Rank.ACE else card.rank.order


@dataclass(frozen=True, slots=True)
class WarRound:
    """一个回合：双方亮的牌、谁赢、这回合押上了多少张。"""

    revealed: tuple[Card, ...]
    winner: int | None
    pot_size: int


class WarGame:
    """战争：两人各一摞牌，同时翻开一张，大的收走；打平就各押三张暗牌再翻一张。

    它用的是和 21 点完全相同的 `Card` 和 `Deck`，一行都没有为它改过。
    """

    def __init__(self, deck: Deck) -> None:
        half = deck.remaining // 2
        if half < 1:
            raise CardGameError("牌太少，开不了局")
        self._piles = (Deck(deck.deal(half)), Deck(deck.deal(half)))

    @property
    def pile_sizes(self) -> tuple[int, int]:
        """两摞牌各剩几张。"""
        return (self._piles[0].remaining, self._piles[1].remaining)

    def play_round(self) -> WarRound:
        """打一个回合。某一方牌不够时，这回合直接判给另一方。

        每一条出口都走 `_award`：押上去的牌一定会回到某个人手里，牌不会在半路消失。
        """
        pot: list[Card] = []
        while True:
            for index, pile in enumerate(self._piles):
                if pile.remaining == 0:
                    return self._award(pot, 1 - index)
            left, right = self._piles[0].deal_one(), self._piles[1].deal_one()
            pot += [left, right]
            if war_order(left) != war_order(right):
                return self._award(pot, 0 if war_order(left) > war_order(right) else 1)
            for index, pile in enumerate(self._piles):
                if pile.remaining < 4:
                    return self._award(pot, 1 - index)
            pot += [*self._piles[0].deal(3), *self._piles[1].deal(3)]

    def _award(self, pot: list[Card], winner: int) -> WarRound:
        """把这一回合押上的牌全部压到赢家的牌堆底下——牌的总数是守恒的。"""
        self._piles[winner].place_at_bottom(sorted(pot))
        return WarRound(tuple(pot), winner, len(pot))

    def play(self, max_rounds: int = 2000) -> int | None:
        """一直打到一方收光，或者回合数耗尽（战争是会打不完的）。返回赢家下标或 `None`。"""
        for _ in range(max_rounds):
            result = self.play_round()
            if 0 in self.pile_sizes:
                return result.winner
        return None


if __name__ == "__main__":  # pragma: no cover - 演示用
    rng = random.Random(42)
    shoe = Shoe(decks=6, rng=rng)
    counter = RunningCount(shoe)
    game = BlackjackGame(shoe, dealer_policy=hit_soft_17)
    for _ in range(5):
        result = game.play_round(stand_on(17))
        print(f"玩家 {result.player}={result.player_total}  庄家 {result.dealer}={result.dealer_total}"
              f"  → {result.outcome.value}  跑动计数 {counter.running:+d}（真数 {counter.true_count:+.2f}）")
    print(f"牌鞋剩 {shoe.remaining} 张，该洗牌了吗：{shoe.needs_shuffle}")

    war_deck = Deck(build_deck())
    war_deck.shuffle(rng)
    war = WarGame(war_deck)
    print(f"战争：同一副牌、同一个 Deck，开局两摞 {war.pile_sizes}，赢家是 {war.play()}")
