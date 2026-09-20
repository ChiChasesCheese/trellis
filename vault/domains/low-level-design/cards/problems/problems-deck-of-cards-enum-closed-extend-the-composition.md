---
id: problems-deck-of-cards-enum-closed-extend-the-composition
node: problems.games.deck-of-cards
type: qa
step: 7
tags: [grown]
---
## Q
扑克牌设计里花色和点数写成 `Enum`。现在要加小丑牌（Joker）或者第五门花色，而且不许改动任何游戏代码。为什么扩展点不能放在枚举上？该放在哪？

## A
因为 Python 的 `Enum` 一旦有了成员就**不能被继承**——`class MoreSuits(Suit)` 直接报错。所以如果造牌代码写成遍历整个枚举：

```python
cards = [Card(r, s) for s in Suit for r in Rank]   # 把牌堆组成钉死在类型上
```

那么「这副牌由哪些牌组成」就被钉死在类型定义上，加一门花色要改枚举，而所有 `for s in Suit` 的地方都会跟着变。

扩展点应该是**牌堆的组成**，也就是一个参数：`build_deck(copies=1, *, ranks=STANDARD_RANKS, suits=STANDARD_SUITS, jokers=0)`，函数遍历传进来的清单而不是枚举。枚举里可以预留 `Suit.STARS` 和 `Rank.JOKER`，但标准清单不含它们。于是加第五门花色是换一个参数，五门花色的牌鞋直接能打 21 点——因为 21 点只读点数、根本不看花色。
