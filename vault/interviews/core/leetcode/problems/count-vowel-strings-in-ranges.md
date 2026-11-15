---
slug: count-vowel-strings-in-ranges
---
## Q
**LC 2559 统计范围内的元音字符串数**｜Medium

字符串数组 `words`，每个查询 `[l, r]` 问下标在 `[l, r]` 内、首尾都是元音的字符串有几个。

## A
**一句话。** 把每个词变成 0/1，建前缀和 `pre`，查询答案是 `pre[r+1] - pre[l]`。

```python
def vowel_strings(words, queries):
    V = set("aeiou")
    pre = [0]                  # pre[i]：前 i 个词中的个数
    for w in words:
        ok = w[0] in V and w[-1] in V
        pre.append(pre[-1] + ok)
    return [pre[r + 1] - pre[l] for l, r in queries]
```

**复杂度。** 时间 `O(n + q)`，空间 `O(n)`。

**易错点。**
- 写成 `pre[r] - pre[l-1]`：`l = 0` 时越界成 `pre[-1]`，前缀和多开一位就是为了避免它。
- 只判断首字母：首尾都要是元音，单字母词 `"e"` 首尾是同一个字符。

**追问。**
- 还会修改 `words`？：单点修改、区间求和，用树状数组，每次 `O(log n)`。
- 查询离线且很多？：前缀和已是 `O(1)` 每次，无需离线。

**同模式。** LC 560 和为 K 的子数组、LC 303 区域和检索 - 数组不可变、LC 1310 子数组异或查询
