---
id: tlc-flip-string-to-monotone-increasing-2-code
node: b.flip-string-to-monotone-increasing
type: qa
step: 2
---
## Q
**LC 926 将字符串翻转到单调递增**｜写出 Python 实现

二进制字符串 `s`（`1 <= s.length <= 10^5`，只含 `'0'` 和 `'1'`）。单调递增指若干个 `0` 后接若干个 `1`。每次可以翻转任意一个字符，返回使 `s` 单调递增的最少翻转次数。

## A
**思路。** 一遍扫描，`ones` 记录已见的 `1` 的个数，`flips` 记录当前前缀单调化的最少翻转次数。遇到 `'1'` 只让 `ones` 加一；遇到 `'0'`，要么把它翻成 `1`（`flips + 1`），要么把前面所有 `1` 翻成 `0`（`ones`），取较小值。

```python
def min_flips_mono_incr(s: str) -> int:
    ones = flips = 0                  # ones：已见的 '1' 数；flips：s[:i] 变成单调递增的最少翻转
    for ch in s:
        if ch == "1":
            ones += 1                 # 追加 '1' 永远不破坏单调，代价不变
        else:
            flips = min(flips + 1, ones)   # 追加 '0'：把它翻成 '1'，或把前面所有 '1' 都翻成 '0'
    return flips
```

运行：`"00110"` → `1`，`"010110"` → `2`，`"00011000"` → `2`，`"1"` → `0`，`"0"` → `0`，`"111000"` → `3`，`"10" * 50000` → `50000`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**写法要点。** `ones = flips = 0` 链式赋值初始化两个计数；直接遍历字符串，不要写下标；`min(flips + 1, ones)` 一个表达式覆盖两种选择，没有分支嵌套；空字符串不在约束内，所以不需要特判；返回的 `flips` 就是答案，不需要再扫一遍。
