---
id: tlc-stickers-to-spell-word-5-alt
node: a.stickers-to-spell-word
type: qa
step: 5
---
## Q
**LC 691 贴纸拼词**｜另一种解法

除了位掩码 DP，还有什么常见解法？什么时候选它？（`1 <= n <= 50`，`1 <= stickers[i].length <= 10`，`1 <= target.length <= 15`）

## A
**记忆化 DFS。** 状态是「还没盖住的字母」排好序后的字符串。取其首字母，只试含该字母的贴纸，每张贴纸扣掉能扣的字母，递归求剩余字符串；结果缓存。

```python
from collections import Counter
from functools import cache
from math import inf


def min_stickers(stickers: list[str], target: str) -> int:
    cnts = [Counter(s) for s in stickers]

    @cache
    def dfs(rest: str) -> int:                       # rest：还没盖住的字母，升序排好当缓存键
        if not rest:
            return 0
        best = inf
        for cnt in cnts:
            if cnt[rest[0]] == 0:                    # 只用能盖住 rest 首字母的贴纸
                continue
            nxt = "".join(ch * (k - cnt[ch]) for ch, k in sorted(Counter(rest).items()) if k > cnt[ch])
            best = min(best, 1 + dfs(nxt))
        return best

    ans = dfs("".join(sorted(target)))
    return -1 if ans == inf else ans
```

`["with","example","science"]`，`"thehat"` → `3`；`["notice","possible"]`，`"basicbasic"` → `-1`；`["ab"]`，`"aa"` → `2`。

**怎么选。**
- DFS 只访问可达的剩余字母多重集合，不必遍历全部 `2^m` 个掩码；可达状态很少时（`target` 里重复字母多、贴纸能一次盖住很多）占优。
- 位掩码 DP 的上界清楚（`2^m * k * m`）、没有递归、常数里没有字符串拼接，`m <= 15` 时更稳；面试默认写它。
- DFS 的缓存键是字符串，每步要重建 `Counter` 和排序，常数更大；`target` 更长时两者都会爆，需要加下界剪枝。
