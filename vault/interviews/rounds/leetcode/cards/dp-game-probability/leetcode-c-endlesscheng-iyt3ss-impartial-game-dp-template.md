---
id: leetcode-c-endlesscheng-iyt3ss-impartial-game-dp-template
node: dp-game-probability.impartial-game-dp
type: cloze
anki: 1787272428304
tags: [concept-cloze, leetcode, recall, template]
---
递归模板中，找到 not win(next_state) 时应立即返回 {{c1::True}}。

```
from functools import cache

def first_player_wins(n, moves):
    @cache
    def win(state):
        for move in moves:
            if move <= state and not win(state - move):
                return True
        return False
    return win(n)
```

**Evidence**

四、博弈论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.12%20-%20%E5%85%AC%E5%B9%B3%E7%BB%84%E5%90%88%E5%8D%9A%E5%BC%88%E7%9A%84%E8%83%9C%E8%B4%9F%20DP)
