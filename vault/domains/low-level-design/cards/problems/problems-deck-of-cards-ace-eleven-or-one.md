---
id: problems-deck-of-cards-ace-eleven-or-one
node: problems.games.deck-of-cards
type: qa
step: 3
tags: [grown]
---
## Q
二十一点（Blackjack）里 A 可以算 11 也可以算 1。流行写法是枚举每张 A 取 1 或 11 的所有组合（n 张 A 就是 2ⁿ 个分数）再挑「不超过 21 的最大值」。为什么这是过度设计？正确的算法是什么？

## A
因为**两张 A 都算 11 就是 22，已经爆了**——所以任何一手牌里最多只有一张 A 能算 11。既然只有两种情况，就不需要搜索：

```python
hard = sum(BLACKJACK_VALUES[c.rank] for c in cards)  # A 一律按 1
if has_ace and hard + 10 <= 21:
    return hard + 10
return hard
```

一次加法、一个布尔判断。用 2ⁿ 枚举去解一个其实只有两种情况的问题，是典型的「没想清楚就先上算法」。

这个写法还白送了 `is_soft`（那个 +10 有没有被加上）——「软 17 要不要继续要牌」恰好是庄家两种标准策略的分水岭，枚举写法要另外写一遍逻辑才知道这件事。
