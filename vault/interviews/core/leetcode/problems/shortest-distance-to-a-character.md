---
slug: shortest-distance-to-a-character
---
## Q
**LC 821 字符的最短距离**｜Easy

字符串 `s` 和一个在 `s` 中出现的字符 `c`。返回数组 `answer`，`answer[i]` 是 `s[i]` 到最近一个 `c` 的距离（下标差的绝对值）。

## A
**一句话。** 两遍扫描：从左到右记「左边最近的 `c`」，从右到左记「右边最近的 `c`」，每个位置取较小的距离。

```python
def shortest_to_char(s, c):
    n = len(s)
    res = [n] * n
    pos = -n                     # 左边还没有 c，距离设成很大
    for i in range(n):
        if s[i] == c:
            pos = i
        res[i] = i - pos
    pos = 2 * n                  # 右边还没有 c
    for i in range(n - 1, -1, -1):
        if s[i] == c:
            pos = i
        res[i] = min(res[i], pos - i)
    return res
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`（不计输出）。

**易错点。**
- 哨兵值太小：`pos` 初值设成 `-1` 时，开头的字符会得到一个很小的假距离，应该设成远超过 `n`。
- 只扫一遍：只看左边或只看右边都会漏掉另一侧更近的 `c`。

**追问。**
- 能一遍扫描吗？：先收集所有 `c` 的下标，再对每个位置用双指针找前后两个 `c`。
- 多源 BFS 能做吗？：把所有 `c` 同时入队向两边扩，结果相同但常数更大。

**同模式。** LC 42 接雨水、LC 135 分发糖果、LC 849 到最近的人的最大距离、LC 542 01 矩阵
