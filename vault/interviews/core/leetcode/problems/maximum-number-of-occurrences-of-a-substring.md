---
slug: maximum-number-of-occurrences-of-a-substring
---
## Q
**LC 1297 子串的最大出现次数**｜Medium

求满足「不同字母数 `<= maxLetters`、长度在 `[minSize, maxSize]`」的子串中，出现次数最多的那个的次数。

## A
**一句话。** 只需看长度恰为 `minSize` 的子串：任何更长的合法子串出现一次，它的前 `minSize` 个字符也合法且至少出现同样多次；定长窗口逐个计数即可。

```python
def max_freq(s, max_letters, min_size, max_size):
    cnt = Counter()
    for i in range(len(s) - min_size + 1):
        sub = s[i:i + min_size]       # 只看最短长度
        if len(set(sub)) <= max_letters:
            cnt[sub] += 1
    return max(cnt.values(), default=0)
```

**复杂度。** 时间 `O(n·minSize)`，空间 `O(n·minSize)`。

**易错点。**
- 枚举所有长度 `minSize..maxSize`：多一层循环，且长度更大的永远不会更多。
- 没有合法子串时 `max` 报错：要给 `default=0`。

**追问。**
- 去掉 `set` 的开销？：滑动窗口维护字母计数和不同字母数，进一个出一个 `O(1)`。
- 子串比较太贵？：用滚动哈希把每个窗口变成一个整数再计数。

**同模式。** LC 438 找到字符串中所有字母异位词、LC 3 无重复字符的最长子串、LC 1461 检查一个字符串是否包含所有长度为 K 的二进制子串
