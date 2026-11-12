---
slug: smallest-subsequence-of-distinct-characters
---
## Q
**LC 1081 不同字符的最小子序列**｜Medium

返回字符串 `s` 中包含每种字符恰好一次的字典序最小的子序列。

## A
**一句话。** 逐位贪心：在「不让任何未放字母丢失」的窗口里选最小的未用字母。

```python
def smallest_subsequence(s):
    last = {ch: i for i, ch in enumerate(s)}   # 最后出现位置
    remaining = set(s)
    res = []
    pos = 0
    while remaining:
        # 选的位置不能超过 deadline，否则某字母再也出现不了
        deadline = min(last[c] for c in remaining)
        # 窗口内最小的未用字母，并列取最靠左
        i = min((j for j in range(pos, deadline + 1)
                 if s[j] in remaining), key=s.__getitem__)
        res.append(s[i])
        remaining.discard(s[i])
        pos = i + 1
    return "".join(res)
```

**复杂度。** 时间 `O(26n)`，空间 `O(26)`。

**易错点。**
- 无视 `deadline` 直接挑全局最小：`"bcab"` 先选 `a`，`c` 再也找不到，得 `"ab"`，应为 `"bca"`。
- 并列不取最靠左：会白白浪费后面的出现位置。
- 窗口里不排除已用字母：会重复选。

**追问。**
- 有更快的写法吗？：单调栈一遍 `O(n)`，遇到更小字母就弹掉后面还会出现的较大栈顶（LC 316）。
- 要字典序最大？：每轮挑窗口里最大的字母，并列仍取最靠左。

**同模式。** LC 316 去除重复字母、LC 402 移掉 K 位数字、LC 321 拼接最大数、LC 738 单调递增的数字
