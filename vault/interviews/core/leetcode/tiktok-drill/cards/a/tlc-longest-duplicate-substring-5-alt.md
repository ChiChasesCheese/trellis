---
id: tlc-longest-duplicate-substring-5-alt
node: a.longest-duplicate-substring
type: qa
step: 5
---
## Q
**LC 1044 最长重复子串**｜另一种解法

不用滚动哈希，用后缀数组（suffix array）加最长公共前缀（LCP）怎么做？它和二分 + 哈希相比，什么时候选哪个？

## A
**思路。** 把所有后缀按字典序排序。一个重复子串必然是两个后缀的公共前缀，而字典序下，公共前缀最长的一对后缀一定相邻。所以答案长度 = 相邻后缀 LCP 的最大值。后缀数组用倍增法排序（每轮按前 `2^k` 个字符的排名对排序），LCP 用 Kasai 算法在 `O(n)` 内算出。

```python
from itertools import pairwise


def longest_dup_substring_sa(s: str) -> str:
    n = len(s)
    rank = [ord(c) for c in s]
    sa = list(range(n))
    k = 1
    while True:                            # 倍增：按 (rank[i], rank[i + k]) 排序
        def key(i: int) -> tuple[int, int]:
            return rank[i], rank[i + k] if i + k < n else -1
        sa.sort(key=key)
        new = [0] * n
        for a, b in pairwise(sa):
            new[b] = new[a] + (key(a) != key(b))
        rank = new
        if rank[sa[-1]] == n - 1:          # 排名全部不同：排序完成
            break
        k <<= 1
    pos = [0] * n                          # pos[i]：后缀 i 在 sa 中的名次
    for r, i in enumerate(sa):
        pos[i] = r
    h = best = start = 0
    for i in range(n):                     # Kasai：h 是后缀 i 与其前一名的 LCP，逐步最多减 1
        if pos[i] == 0:
            h = 0
            continue
        j = sa[pos[i] - 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        if h > best:
            best, start = h, i
        if h:
            h -= 1
    return s[start:start + best]
```

运行：`"banana"` → `'ana'`，`"abcd"` → `''`；长度 `30000` 的随机小写串和全 `a` 串都能在 `n = 3 * 10^4` 的限制内完成。

**为什么对。** 排序后相邻的后缀共享的前缀最长（字典序性质：若 `A < B < C`，则 `LCP(A, C) = min(LCP(A, B), LCP(B, C))`），所以最大的重复前缀必在某对相邻后缀中；两个不同起点的后缀的公共前缀就是一个出现两次的子串，允许重叠自然成立。Kasai 利用 `LCP(后缀 i+1) >= LCP(后缀 i) - 1`，所以 `h` 每步最多减 `1`，总移动 `O(n)`。

**取舍。** 二分 + 滚动哈希：代码短、期望 `O(n log n)`，有极小的碰撞概率，面试里最常见。后缀数组：确定性、没有概率，能顺带解决「最长公共子串」「不同子串个数」等一族问题，倍增排序 `O(n log^2 n)`；代码长、易写错，适合被追问「不要概率」时提出。
