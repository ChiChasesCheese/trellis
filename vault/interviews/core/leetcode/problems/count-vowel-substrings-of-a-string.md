---
slug: count-vowel-substrings-of-a-string
---
## Q
**LC 2062 统计字符串中的元音子字符串**｜Easy

统计 `word` 中仅由元音组成、且五种元音（`aeiou`）都出现的子串个数。

## A
**一句话。** 辅音把串切成纯元音段，段内对每个右端点 `i`，合法左端点为 `[段起点, 五元音最后位置的最小值]`。

```python
def count_vowel_substrings(word):
    ans = start = 0              # start：当前元音段起点
    last = dict.fromkeys("aeiou", -1)
    for i, ch in enumerate(word):
        if ch not in last:       # 辅音：整段重置
            start = i + 1
            last = dict.fromkeys("aeiou", -1)
            continue
        last[ch] = i
        lo = min(last.values())
        if lo >= start:          # 五个元音段内都出现过
            ans += lo - start + 1
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 辅音不重置 `last` 和 `start`：`"bbaeixoubb"` 把含 `x` 的串数进去，得 `3`，应为 `0`。
- 漏掉 `lo >= start`：某元音未出现时 `lo=-1`，`"baei"` 累加成负数。
- 每段只数一次：`"aeiouu"` 得 `1`，应为 `2`。

**追问。**
- 恰好含 `k` 种元音？：改用 `至多 k 种 − 至多 k-1 种` 的滑动窗口差。
- `n` 很大怎么办？：本解已 `O(n)`；`n<=100` 时暴力枚举也行。

**同模式。** LC 2063 所有子字符串中的元音、LC 992 K 个不同整数的子数组、LC 1456 定长子串中元音的最大数目、LC 3 无重复字符的最长子串
