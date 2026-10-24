---
id: tlc-minimum-window-substring-2-code
node: a.minimum-window-substring
type: qa
step: 2
---
## Q
**LC 76 最小覆盖子串**｜写出 Python 实现

`s` 和 `t` 由英文字母组成，长度 `1 <= m, n <= 10^5`。返回 `s` 中包含 `t` 全部字符（含重复）的最短子串，不存在返回 `""`。要求 `O(m + n)`。

## A
**思路。** `need` 记录每个字符还差多少（负数表示窗口里多出来），`missing` 记录总共还缺多少个。右端逐个加入字符；`missing == 0` 时先把左端多余的字符丢掉，更新最短窗口，再丢掉一个必需字符，让窗口重新变得不完整，继续向右。

```python
from collections import Counter


def min_window(s: str, t: str) -> str:
    need = Counter(t)                              # need[ch] > 0 表示还缺 ch；< 0 表示窗口里多出来
    missing = len(t)                               # 还缺的字符总数（含重复）
    best_l, best_len = 0, len(s) + 1
    left = 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:                           # 窗口已经覆盖 t：尽量收缩左端
            while need[s[left]] < 0:               # 左端字符是多余的，丢掉
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best_len:
                best_l, best_len = left, right - left + 1
            need[s[left]] += 1                     # 再丢一个必需字符，窗口重新变得不完整
            missing += 1
            left += 1
    return "" if best_len > len(s) else s[best_l : best_l + best_len]
```

运行：`"ADOBECODEBANC", "ABC"` → `"BANC"`；`"a", "a"` → `"a"`；`"a", "aa"` → `""`；`"aa", "aa"` → `"aa"`；`"ab", "b"` → `"b"`；`"bba", "ab"` → `"ba"`。

**复杂度。** 时间 `O(m + n)`：每个下标进窗口一次、出窗口至多一次；空间 `O(Σ)`，`Σ` 是字母表大小。

**写法要点。** `Counter(t)` 一步建出需求表，且对不存在的键读取返回 `0`，不抛 `KeyError`；`need` 里存「欠额」，正数缺、负数溢出，一个数同时表达两种状态，所以不需要第二个表；`missing` 只在 `need[ch] > 0` 时才变化，把"是否覆盖"从 `O(Σ)` 的比较变成 `O(1)`；`best_len` 初值取 `len(s) + 1` 作为"没找到"的哨兵；切片只在最后做一次。
