---
nodes: [problems.games.deck-of-cards]
url: https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design/deck_of_cards
---
# system-design-primer — object_oriented_design/deck_of_cards

值得读：被引用最多的那份 Python 实现，也是本题解最主要的**反面参照**。`Card` 是抽象基类、
`BlackJackCard` 是它的子类并且带一个可写的 `value`，`Hand.cards` 是公开的可变列表，21 点的
点数用 `possible_scores()` 枚举每张 A 取 1 或 11 的所有组合再挑最优，牌上还挂着
`is_available` 这个状态。本题解在四处反过来做：规则从 `Card` 移到游戏自己的取值表（否则
第二个游戏无处安放——战争里 A 最大、21 点里 A 是 1 或 11）、`Deck` 不交出内部列表、A 的点数
用"最多一张 A 能算 11"的一次加法代替 2ⁿ 枚举、牌是 `frozen` 的值对象（没有 setter，
"有没有被发出去"是牌堆的状态而不是牌的状态）。仓库根目录的 `LICENSE.txt` 是 CC BY 4.0。
