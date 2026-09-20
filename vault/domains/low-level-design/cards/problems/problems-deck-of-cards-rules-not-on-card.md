---
id: problems-deck-of-cards-rules-not-on-card
node: problems.games.deck-of-cards
type: qa
step: 1
tags: [grown]
---
## Q
设计一副扑克牌（Deck of Cards）并在上面实现二十一点（Blackjack）。最常见的写法是给 `Card` 加一个 `value` 属性，或者写一个 `BlackJackCard(Card)` 子类。为什么这是这道题的头号失分点？

## A
因为它把一副**通用**的扑克牌变成了一副只能打 21 点的牌，而且不可逆。

第二个游戏一来就崩：战争（War）里 A 最大、21 点里 A 是 1 或 11、斗地主里 2 比 A 大。是再写一个 `WarCard(Card)` 吗？那牌堆里到底装的是哪一种卡、`Deck` 岂不是要知道自己为哪个游戏服务？而且 `value` 这个名字本身就错——A 的值不是一个数，是两个候选，所以那份写法不得不再写一个 `possible_scores()` 去纠正它。**当一个属性必须被另一个方法纠正时，这个属性就不该存在。**

正确的分界线：`Card` 是一个不可变的值（只有 `rank` 和 `suit`），规则是**游戏自己的一张表**，比如 `BLACKJACK_VALUES: Mapping[Rank, int]` 和 `war_order(card) -> int`。检验标准一句话：**如果一个属性的正确值取决于现在在玩哪个游戏，它就不属于 `Card`。**
