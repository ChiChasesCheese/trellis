---
slug: count-binary-substrings
---
## Q
**LC 696 计数二进制子串**｜Easy

`01` 串 `s` 中，统计 `0` 和 `1` 数量相等、且各自连续成组的非空子串个数（不同位置的相同子串重复计数）。

## A
**一句话。** 按连续相同字符分段，相邻两段贡献 `min(前段长, 后段长)` 个合法子串，累加。

```python
def count_binary_substrings(s):
    res, prev, cur = 0, 0, 1     # prev 上一段长，cur 当前段长
    for a, b in pairwise(s):
        if a == b:
            cur += 1
        else:
            res += min(prev, cur)
            prev, cur = cur, 1
    return res + min(prev, cur)  # 最后一对相邻段
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 循环后漏加最后一对：`"0011"` 只有一个边界，贡献全在最后的 `min(prev, cur)`，漏掉得 `0`，应为 `2`。
- `prev` 初值取 `1`：第一段前没有段，`"0011"` 会得 `3`，应为 `0`。

**追问。**
- 要返回所有合法子串？：对每个边界取 `1..min(prev, cur)` 切出，输出规模 `O(n²)` 字符。
- 流式输入能做吗？：只存 `prev` 和 `cur`，天然支持。

**同模式。** LC 695 岛屿的最大面积、LC 485 最大连续 1 的个数、LC 647 回文子串、LC 5 最长回文子串
