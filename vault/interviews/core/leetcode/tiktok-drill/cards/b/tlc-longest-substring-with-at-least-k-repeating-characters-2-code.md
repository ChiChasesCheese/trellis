---
id: tlc-longest-substring-with-at-least-k-repeating-characters-2-code
node: b.longest-substring-with-at-least-k-repeating-characters
type: qa
step: 2
---
## Q
**LC 395 至少有 K 个重复字符的最长子串**｜写出 Python 实现

`s` 仅含小写字母（长度 `1` 到 `10^4`），整数 `k`（`1 <= k <= 10^5`）。求最长子串长度，使子串里每个字符出现次数都不少于 `k`；不存在则返回 `0`。

## A
**思路。** 统计整串各字符次数。若所有字符次数都 `>= k`，整串就是答案。否则任选一个次数 `< k` 的字符 `bad`，答案不会包含它，按 `bad` 切开，对每段递归，取最大值。

```python
from collections import Counter

def longest_substring(s: str, k: int) -> int:
    if len(s) < k:
        return 0
    count = Counter(s)
    bad = next((ch for ch, c in count.items() if c < k), None)   # 任意一个出现次数不足 k 的字符
    if bad is None:
        return len(s)                          # 整串已经合法
    return max(longest_substring(part, k) for part in s.split(bad))   # 含 bad 的子串一定不合法，按它切开
```

运行：`("aaabb", 3)` → `3`，`("ababbc", 2)` → `5`，`("a", 2)` → `0`，`("a", 1)` → `1`，`("abc", 100000)` → `0`，`("aaacbbb", 3)` → `3`。

**复杂度。** 时间 `O(26 · n)`：递归深度不超过字符种数 `26`，每层所有段的总长度不超过 `n`，每段 `Counter` 线性；空间 `O(n)`：切片产生的子串。

**写法要点。** `next(生成器, None)` 取第一个满足条件的元素，没有时给默认值，比先建列表再取 `[0]` 干净；`s.split(bad)` 一步完成「按字符切开」，空段会自然返回 `0`；`max(生成器)` 在 `split` 至少有两段时不会为空；`Counter` 的 `items()` 遍历顺序是首次出现的顺序，选哪个 `bad` 不影响结果。
