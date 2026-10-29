---
id: tlc-valid-anagram-2-code
node: b.valid-anagram
type: qa
step: 2
---
## Q
**LC 242 有效的字母异位词**｜写出 Python 实现

两个只含小写字母的字符串 `s`、`t`（长度 `1` 到 `5 * 10^4`），判断 `t` 是否是 `s` 的字母异位词。要求 `O(n)`，并且不依赖「只有 26 个字母」。

## A
**思路。** 长度不同直接返回 `False`。用 `Counter(s)` 计数，再扫 `t` 逐个减一，某个计数变成负数说明 `t` 里这个字符多了。长度相等又没有负数，所有计数只能都是 0。

```python
from collections import Counter


def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):                 # 长度不同直接否；也是下面「没出现负数」能推出「全为 0」的前提
        return False
    count = Counter(s)                   # 字符 -> 它在 s 里的出现次数
    for ch in t:
        count[ch] -= 1
        if count[ch] < 0:                # t 里的 ch 比 s 多
            return False
    return True
```

运行：`"anagram", "nagaram"` → `True`，`"rat", "car"` → `False`，`"a", "a"` → `True`，`"ab", "a"` → `False`，`"aab", "abb"` → `False`。

**复杂度。** 时间 `O(n)`；空间 `O(Σ)`，`Σ` 是出现过的字符种类数。

**写法要点。** `Counter` 访问不存在的键返回 `0` 而不是抛 `KeyError`，`count[ch] -= 1` 不用先判断；不需要提前返回时，`Counter(s) == Counter(t)` 一行也是地道写法（3.10 起计数为 0 的键与缺失的键视为相等）；只有小写字母时也可以用 `[0] * 26` 加 `ord(ch) - ord("a")`，常数更小但换了字符集就不能用。
