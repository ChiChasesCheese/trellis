---
id: tlc-longest-substring-with-at-most-k-distinct-characters-2-code
node: p2.longest-substring-with-at-most-k-distinct-characters
type: qa
step: 2
---
## Q
**LC 340 至多包含 K 个不同字符的最长子串**｜写出 Python 实现

字符串 `s`（长度 `1` 到 `5 * 10^4`）和整数 `k`（`0` 到 `50`），返回至多包含 `k` 个不同字符的最长子串的长度。要求 `O(n)`。

## A
**思路。** `Counter` 记录窗口内各字符的出现次数。右端加入字符后，若不同字符种类数 `len(count)` 超过 `k`，就从左端逐个移除字符，计数为 `0` 时删除该键，直到种类数不超过 `k`。窗口合法后用长度更新答案。

```python
from collections import Counter

def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    count: Counter[str] = Counter()         # 窗口内每个字符的出现次数
    left = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:               # 种类超了：缩左端，计数归零就删键，len 才准
            out = s[left]
            count[out] -= 1
            if count[out] == 0:
                del count[out]
            left += 1
        best = max(best, right - left + 1)
    return best
```

运行：`("eceba", 2)` → `3`，`("aa", 1)` → `2`，`("abc", 0)` → `0`，`("a", 5)` → `1`。

**复杂度。** 时间 `O(n)`：每个字符进窗口、出窗口各一次，每步字典操作 `O(1)`；空间 `O(k)`：计数器至多 `k + 1` 个键。

**写法要点。**
- `Counter` 读取、递增不存在的键都不会报错，`count[ch] += 1` 一行完成“出现则加一、首次则初始为一”。
- 计数归零必须 `del`：`Counter` 不会自动删除零计数的键，`len(count)` 才是窗口内的真实种类数。
- 变量名 `out` 表示被移出窗口的字符；`s[left]` 先取出再 `left += 1`，顺序不能反。
- `for right, ch in enumerate(s)` 让右端由循环驱动，左端用 `while` 手动推进，各自只前进。
- 类型标注 `Counter[str]` 在 Python 3.9 以上可以直接对 `collections.Counter` 下标。
