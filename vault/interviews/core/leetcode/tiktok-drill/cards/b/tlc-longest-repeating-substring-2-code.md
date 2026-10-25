---
id: tlc-longest-repeating-substring-2-code
node: b.longest-repeating-substring
type: qa
step: 2
---
## Q
**LC 1062 最长重复子串**｜写出 Python 实现

小写字母字符串 `s`（长度 `1` 到 `2000`）。返回最长重复子串的长度：在 `s` 中出现至少两次的连续子串（两次出现可以重叠），没有则返回 `0`。

## A
**思路。** 在 `[0, n-1]` 上二分答案长度。`has_repeat(L)` 扫描所有长度为 `L` 的窗口，放进集合，见到已有的就返回真。可行就把下界抬到 `mid`，否则把上界降到 `mid - 1`；中点上取整保证区间一定收缩。

```python
def longest_repeating_substring(s: str) -> int:
    def has_repeat(length: int) -> bool:   # 是否存在长度为 length 的子串出现至少两次（可重叠）
        seen: set[str] = set()
        for i in range(len(s) - length + 1):
            sub = s[i:i + length]
            if sub in seen:
                return True
            seen.add(sub)
        return False

    lo, hi = 0, len(s) - 1                 # 答案在 [0, n-1]；长度 0 总是可行
    while lo < hi:
        mid = (lo + hi + 1) // 2           # 上取整，避免 lo = mid 时死循环
        if has_repeat(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

运行：`"abcd"` → `0`，`"abbaba"` → `2`，`"aabcaabdaab"` → `3`，`"a"` → `0`，`"aaaa"` → `3`。

**复杂度。** 时间 `O(n^2 log n)`：约 `11` 轮二分，每轮 `O(n)` 个窗口，每个窗口切片与哈希 `O(L)`；空间最坏 `O(n^2)`（集合里存 `n` 个长度接近 `n` 的串）。

**写法要点。** 嵌套函数 `has_repeat` 直接读取外层的 `s`；`set[str]` 的 `in` 是均摊 `O(1)`，先查后加，遇到重复立即返回；「找最大的可行值」用 `lo = mid` / `hi = mid - 1` 的上取整模板，与「找最小可行值」的 `lo = mid + 1` / `hi = mid` 对称；把单调的判定写成独立函数，二分部分只有 `6` 行，不易写错。
