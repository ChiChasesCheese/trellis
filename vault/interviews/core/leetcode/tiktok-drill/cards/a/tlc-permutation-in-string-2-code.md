---
id: tlc-permutation-in-string-2-code
node: a.permutation-in-string
type: qa
step: 2
---
## Q
**LC 567 字符串的排列**｜写出 Python 实现

字符串 `s1`、`s2`（长度都在 `[1, 10^4]`，只含小写字母），判断 `s2` 是否有某个子串是 `s1` 的排列。要求线性时间。

## A
**思路。** 窗口长度固定为 `m = len(s1)`。`cnt[c]` 记录「`s1` 中 `c` 的个数减窗口中 `c` 的个数」，`diff` 记录 `cnt` 里非零项的个数。先装满第一个窗口；之后每滑一格，加入 `s2[i]`、移出 `s2[i - m]`，只修正这两个字母对 `diff` 的贡献。

```python
def check_inclusion(s1: str, s2: str) -> bool:
    m = len(s1)
    if m > len(s2):
        return False
    cnt = [0] * 26                              # cnt[c] = s1 中 c 的个数 - 窗口中 c 的个数
    for a, b in zip(s1, s2):                    # zip 在较短的 s1 处截断，正好装满第一个窗口
        cnt[ord(a) - 97] += 1
        cnt[ord(b) - 97] -= 1
    diff = sum(c != 0 for c in cnt)             # 个数不匹配的字母种数；0 表示窗口是 s1 的排列
    for i in range(m, len(s2)):
        if diff == 0:
            return True
        for k, d in ((ord(s2[i]) - 97, -1), (ord(s2[i - m]) - 97, 1)):  # 进一个、出一个
            diff -= cnt[k] != 0
            cnt[k] += d
            diff += cnt[k] != 0
    return diff == 0
```

运行：`("ab", "eidbaooo")` → `True`；`("ab", "eidboaoo")` → `False`；`("a", "a")` → `True`；`("abc", "ab")` → `False`；`("ab", "ab")` → `True`；`("adc", "dcda")` → `True`。

**复杂度。** 时间 `O(m + n)`：装第一个窗口 `O(m)`，之后每格 `O(1)`；空间 `O(1)`：26 个计数。

**写法要点。** `zip(s1, s2)` 在较短的序列处停止，一次循环同时初始化「`s1` 计数」与「第一个窗口计数」；`diff -= cnt[k] != 0` 用到 `bool` 是 `int` 的子类，改前减去旧状态、改后加上新状态，不需要写 `if`；`ord(c) - 97` 把小写字母映射到 `0..25`。
