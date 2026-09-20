"""扑克牌与二十一点参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。

随机性有两处：洗牌和牌鞋。断言具体结局的用例一律用"什么都不洗的随机源 + 定死的牌序"，
只有统计性的用例才用带种子的 `random.Random`，而且断言的仍然是与种子无关的不变量（牌不会
凭空多出来、发出去的和剩下的加起来等于总数）。
"""

import importlib
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


class NoShuffle:
    """一个什么都不洗的随机源：让牌鞋严格按给定顺序发牌。"""

    def shuffle(self, seq):
        return None


def card(rank_name, suit_name="CLUBS"):
    return impl.Card(impl.Rank[rank_name], impl.Suit[suit_name])


def scripted_shoe(cards, **kwargs):
    """一只按 `cards` 顺序发牌的牌鞋（`cards[0]` 最先发出）。"""
    contents = tuple(reversed(list(cards)))
    return impl.Shoe(1, rng=NoShuffle(), builder=lambda: contents, **kwargs)


# ---- 第 1 关：牌是不可变值对象 --------------------------------------------


def test_a_card_is_immutable_hashable_and_readable():
    ace = card("ACE", "SPADES")
    assert repr(ace) == "A♠"
    assert ace == card("ACE", "SPADES")
    assert len({ace, card("ACE", "SPADES"), card("ACE", "HEARTS")}) == 2
    with pytest.raises(AttributeError):
        ace.rank = impl.Rank.KING


def test_cards_sort_by_the_printed_order_not_by_any_games_value():
    hand = [card("KING", "SPADES"), card("ACE", "CLUBS"), card("TEN", "HEARTS")]
    assert [repr(c) for c in sorted(hand)] == ["A♣", "10♥", "K♠"]


def test_the_same_card_is_ordered_differently_by_a_game():
    """A 在牌面自然顺序里最小，在战争里最大——所以"大小"不能长在 Card 上。"""
    ace, king = card("ACE", "SPADES"), card("KING", "SPADES")
    assert ace < king
    assert impl.war_order(ace) > impl.war_order(king)


def test_a_standard_deck_has_fifty_two_distinct_cards():
    cards = impl.build_deck()
    assert len(cards) == 52
    assert len(set(cards)) == 52
    assert sum(1 for c in cards if c.suit is impl.Suit.SPADES) == 13


def test_two_copies_make_one_hundred_and_four_cards():
    assert len(impl.build_deck(2)) == 104
    assert len(set(impl.build_deck(2))) == 52


# ---- 第 1 关：牌堆 ---------------------------------------------------------


def test_the_decks_public_surface_is_exactly_its_contract():
    """牌堆承诺的就这五件事。多出来的任何公开名字都是一条绕过封装的路。"""
    deck = impl.Deck(impl.build_deck())
    assert deck.remaining == 52
    assert {name for name in dir(deck) if not name.startswith("_")} == {
        "remaining",
        "shuffle",
        "deal",
        "deal_one",
        "place_at_bottom",
    }


def test_every_card_leaves_the_deck_through_deal_exactly_once():
    """发牌是牌离开牌堆的唯一出口：52 张不重不漏，发完就空。"""
    deck = impl.Deck(impl.build_deck())
    out = []
    while deck.remaining:
        out.extend(deck.deal(min(7, deck.remaining)))
    assert len(out) == 52 and len(set(out)) == 52
    with pytest.raises(impl.OutOfCardsError):
        deck.deal_one()


def test_dealing_takes_from_the_top_in_order_and_shrinks_the_deck():
    deck = impl.Deck([card("TWO"), card("THREE"), card("FOUR")])
    assert repr(deck.deal_one()) == "4♣"
    assert [repr(c) for c in deck.deal(2)] == ["3♣", "2♣"]
    assert deck.remaining == 0


def test_dealing_from_an_empty_deck_has_a_name():
    deck = impl.Deck()
    with pytest.raises(impl.OutOfCardsError):
        deck.deal_one()


def test_asking_for_more_cards_than_there_are_deals_none_of_them():
    """半成功是最难排查的失败：要 5 张只剩 3 张时一张都不发，牌堆原封不动。"""
    deck = impl.Deck([card("TWO"), card("THREE"), card("FOUR")])
    with pytest.raises(impl.OutOfCardsError):
        deck.deal(5)
    assert deck.remaining == 3
    assert [repr(c) for c in deck.deal(3)] == ["4♣", "3♣", "2♣"]


def test_shuffling_is_reproducible_because_the_source_is_injected():
    def shuffled(seed):
        deck = impl.Deck(impl.build_deck())
        deck.shuffle(random.Random(seed))
        return [repr(c) for c in deck.deal(52)]

    assert shuffled(7) == shuffled(7)
    assert shuffled(7) != shuffled(8)


def test_cards_put_back_go_under_the_deck():
    deck = impl.Deck([card("TWO"), card("THREE")])
    deck.place_at_bottom([card("ACE")])
    assert repr(deck.deal_one()) == "3♣"
    assert [repr(c) for c in deck.deal(2)] == ["2♣", "A♣"]


# ---- 第 2 关：二十一点的点数规则 -------------------------------------------


def test_an_ace_counts_eleven_until_it_would_bust():
    assert impl.BlackjackHand([card("ACE"), card("SIX")]).total == 17
    assert impl.BlackjackHand([card("ACE"), card("SIX"), card("KING")]).total == 17
    assert impl.BlackjackHand([card("ACE"), card("ACE")]).total == 12
    assert impl.BlackjackHand([card("ACE"), card("ACE"), card("NINE")]).total == 21


def test_soft_means_an_ace_is_currently_worth_eleven():
    assert impl.BlackjackHand([card("ACE"), card("SIX")]).is_soft is True
    assert impl.BlackjackHand([card("ACE"), card("SIX"), card("KING")]).is_soft is False
    assert impl.BlackjackHand([card("TEN"), card("SEVEN")]).is_soft is False


def test_blackjack_needs_exactly_two_cards_and_bust_is_over_twenty_one():
    assert impl.BlackjackHand([card("ACE"), card("KING")]).is_blackjack is True
    triple = impl.BlackjackHand([card("SEVEN"), card("SEVEN"), card("SEVEN")])
    assert triple.total == 21 and triple.is_blackjack is False
    busted = impl.BlackjackHand([card("KING"), card("QUEEN"), card("TWO")])
    assert busted.is_bust is True and busted.total == 22


def test_a_hand_refuses_a_card_the_game_has_no_value_for():
    hand = impl.BlackjackHand()
    with pytest.raises(impl.UnsupportedCardError):
        hand.add(card("JOKER", "SPADES"))
    assert len(hand) == 0


def test_the_dealer_policy_is_swappable_and_only_soft_seventeen_tells_them_apart():
    soft17 = impl.BlackjackHand([card("ACE"), card("SIX")])
    hard17 = impl.BlackjackHand([card("TEN"), card("SEVEN")])
    assert impl.stand_on_17(soft17) is False
    assert impl.hit_soft_17(soft17) is True
    assert impl.stand_on_17(hard17) is impl.hit_soft_17(hard17) is False


@pytest.mark.parametrize(
    "script, outcome",
    [
        (["ACE", "KING", "NINE", "SEVEN"], "PLAYER_BLACKJACK"),
        (["ACE", "KING", "ACE", "QUEEN"], "PUSH"),
        (["NINE", "EIGHT", "ACE", "QUEEN"], "DEALER_WIN"),
        (["TEN", "SIX", "NINE", "SEVEN", "TEN"], "DEALER_WIN"),
        (["KING", "NINE", "TEN", "SIX", "TEN"], "PLAYER_WIN"),
        (["KING", "NINE", "TEN", "NINE"], "PUSH"),
    ],
)
def test_a_round_is_settled_in_the_right_order(script, outcome):
    shoe = scripted_shoe([card(name) for name in script])
    result = impl.BlackjackGame(shoe).play_round(impl.stand_on(17))
    assert result.outcome is impl.Outcome[outcome]


def test_swapping_the_dealer_policy_changes_the_result_of_the_same_deal():
    script = ["KING", "SEVEN", "ACE", "SIX", "THREE"]
    conservative = impl.BlackjackGame(scripted_shoe([card(n) for n in script]))
    assert conservative.play_round(impl.stand_on(17)).outcome is impl.Outcome.PUSH
    aggressive = impl.BlackjackGame(
        scripted_shoe([card(n) for n in script]), dealer_policy=impl.hit_soft_17
    )
    assert aggressive.play_round(impl.stand_on(17)).outcome is impl.Outcome.DEALER_WIN


# ---- 第 2 关：第二个游戏用同一副牌 ----------------------------------------


def test_war_uses_the_same_deck_and_conserves_every_card():
    deck = impl.Deck(impl.build_deck())
    deck.shuffle(random.Random(3))
    war = impl.WarGame(deck)
    assert war.pile_sizes == (26, 26)
    for _ in range(10):
        result = war.play_round()
        assert result.winner in (0, 1)
        assert sum(war.pile_sizes) == 52


def test_war_finishes_or_says_it_did_not_and_never_loses_a_card():
    for seed in range(12):
        deck = impl.Deck(impl.build_deck())
        deck.shuffle(random.Random(seed))
        war = impl.WarGame(deck)
        winner = war.play(max_rounds=2000)
        assert winner in (0, 1, None)
        assert sum(war.pile_sizes) == 52, "押上去的牌必须回到某个人手里"


# ---- 第 3 关：牌鞋、切牌与算牌 ---------------------------------------------


def test_the_cut_card_asks_for_a_shuffle_but_never_shuffles_mid_hand():
    shoe = scripted_shoe([card("TWO") for _ in range(8)], penetration=0.5)
    assert shoe.needs_shuffle is False
    shoe.deal(3)
    assert shoe.remaining == 5 and shoe.needs_shuffle is False
    shoe.deal(1)
    assert shoe.remaining == 4 and shoe.needs_shuffle is True


def test_every_card_dealt_by_the_shoe_is_accounted_for():
    seen = []
    shoe = impl.Shoe(2, rng=random.Random(1))
    shoe.subscribe(lambda e: seen.extend(e.cards))
    for _ in range(20):
        shoe.deal(3)
    assert len(seen) == 60
    assert shoe.remaining + len(seen) == 104


def test_the_running_count_is_an_observer_and_resets_on_a_shuffle():
    shoe = scripted_shoe([card("FIVE"), card("TWO"), card("KING"), card("EIGHT")])
    counter = impl.RunningCount(shoe)
    shoe.deal(2)
    assert counter.running == 2
    shoe.deal(2)
    assert counter.running == 1
    shoe.shuffle()
    assert counter.running == 0
    shoe.deal(1)
    assert counter.running == 1


def test_a_counter_attached_late_starts_from_zero_and_can_detach():
    shoe = scripted_shoe([card("FIVE") for _ in range(6)])
    shoe.deal(2)
    counter = impl.RunningCount(shoe)
    assert counter.running == 0
    shoe.deal(1)
    assert counter.running == 1
    counter.detach()
    shoe.deal(1)
    assert counter.running == 1


def test_the_true_count_divides_by_the_decks_that_are_left():
    shoe = impl.Shoe(4, rng=random.Random(2))
    counter = impl.RunningCount(shoe)
    shoe.deal(104)
    assert shoe.decks_remaining == pytest.approx(2.0)
    assert counter.true_count == pytest.approx(counter.running / 2.0)


# ---- 第 4 关：换牌堆的组成，游戏一行不改 -----------------------------------


def test_a_fifth_suit_is_added_without_touching_any_game():
    suits = (*impl.Suit, )
    cards = impl.build_deck(suits=suits)
    assert len(cards) == 65
    shoe = impl.Shoe(1, rng=random.Random(4), builder=lambda: cards)
    result = impl.BlackjackGame(shoe).play_round(impl.stand_on(17))
    assert result.outcome in set(impl.Outcome)
    assert result.player_total >= 4


def test_jokers_are_added_to_the_deck_and_refused_loudly_by_blackjack():
    cards = impl.build_deck(jokers=2)
    assert len(cards) == 54
    assert sum(1 for c in cards if c.rank is impl.Rank.JOKER) == 2
    shoe = scripted_shoe([card("JOKER", "SPADES"), card("KING"), card("NINE"), card("SEVEN")])
    with pytest.raises(impl.UnsupportedCardError):
        impl.BlackjackGame(shoe).play_round(impl.stand_on(17))


def test_a_round_is_refused_when_the_shoe_is_nearly_empty():
    shoe = scripted_shoe([card("TWO"), card("THREE"), card("FOUR")])
    with pytest.raises(impl.GameStateError):
        impl.BlackjackGame(shoe).play_round(impl.stand_on(17))


def test_seeded_games_stay_within_the_rules_for_every_seed():
    """跑三十只带种子的牌鞋，断言的全是与种子无关的不变量。"""
    for seed in range(30):
        shoe = impl.Shoe(2, rng=random.Random(seed))
        counter = impl.RunningCount(shoe)
        game = impl.BlackjackGame(shoe, dealer_policy=impl.hit_soft_17)
        for _ in range(10):
            if shoe.remaining < 12:
                shoe.shuffle()
            result = game.play_round(impl.stand_on(17))
            assert result.outcome in set(impl.Outcome)
            assert len(result.player) >= 2 and len(result.dealer) >= 2
            assert result.player_total <= 30 and result.dealer_total <= 30
            if result.outcome is impl.Outcome.PLAYER_BLACKJACK:
                assert result.player_total == 21 and len(result.player) == 2
        assert -104 <= counter.running <= 104
