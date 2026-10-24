---
id: tlc-patterns-sliding-window-4-cover
node: patterns.sliding-window
type: qa
step: 4
---
## Q
**滑动窗口（Sliding Window）｜覆盖型窗口：最小覆盖子串（LC 76）**

要求窗口包含 `t` 的所有字符（含重复），怎样在 `O(1)` 内判断窗口是否已覆盖，而不是每步比较两个 `Counter`？

## A
`need[ch]` = 还需要多少个 `ch`（可以变成负数，表示多余），`missing` = 还差的字符总数。

```python
from collections import Counter
def min_window(s: str, t: str) -> str:
    need = Counter(t)
    missing = len(t)                       # 还差多少个字符（含重复）
    left = 0
    best_l, best_r = 0, len(s) + 1
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1                   # 这个字符是需要的
        need[ch] -= 1                      # 不在 t 里的字符会变成负数，不影响判断
        if missing == 0:                   # 已覆盖
            while need[s[left]] < 0:       # 左端是多余字符：安全缩小
                need[s[left]] += 1
                left += 1
            if right - left < best_r - best_l:
                best_l, best_r = left, right
            need[s[left]] += 1             # 弹出左端，窗口不再覆盖
            missing += 1
            left += 1
    return "" if best_r > len(s) else s[best_l:best_r + 1]
print(min_window("ADOBECODEBANC", "ABC"), min_window("a", "a"), repr(min_window("a", "aa")))
# BANC a ''
```

- 判断覆盖只看一个整数 `missing`，每一步 `O(1)`，总时间 `O(m + n)`，空间 `O(字符集)`。
- `need[ch] < 0` 表示窗口里 `ch` 多了，可以丢；`need[ch] == 0` 表示刚好；`> 0` 才是缺。
- 对比朴素写法 `not (need - window)`：每步 `O(字符集)`，`n = 10^5` 时会慢很多；但字符集只有 52 时也能过。
- 写法顺序：先扩右端、再看是否覆盖、再缩左端并更新答案——这是「最短」窗口的写法。
