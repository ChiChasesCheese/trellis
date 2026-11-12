---
slug: hand-of-straights
---
## Q
**LC 846 一手顺子**｜Medium

判断 `hand` 能否分成若干组，每组恰好 `groupSize` 张连续数值的牌。

## A
**一句话。** 贪心：从小到大处理，当前最小值剩 `c` 张就必须开 `c` 组，把它起头的整段各扣 `c` 张，扣不够即失败。

```python
def is_n_straight_hand(hand, groupSize):
    if len(hand) % groupSize:
        return False
    cnt = Counter(hand)
    for x in sorted(cnt):         # x 是剩余牌里最小的
        c = cnt[x]
        if c == 0:
            continue
        for y in range(x, x + groupSize):
            if cnt[y] < c:        # 缺牌
                return False
            cnt[y] -= c
    return True
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 只判断牌数整除 `groupSize`：`[1,3,5,7]`、`2` 会返回 `True`，应为 `False`。
- 不按升序处理：`[2,3,4,1,2,3]`、`3` 先从 `2` 开组会误判 `False`。
- 扣牌前不查 `cnt[y] < c`：计数变负不报错，`[1,3]`、`2` 返回 `True`。

**追问。**
- 为什么贪心正确？：最小的牌只能当某组的起点，别无选择。
- 数值范围很大也能做吗？：能，`Counter` 只存出现过的值，再排序它的键。

**同模式。** LC 1296 划分数组为连续数字的集合、LC 659 分割数组为连续子序列、LC 1743 从相邻元素对还原数组、LC 128 最长连续序列
