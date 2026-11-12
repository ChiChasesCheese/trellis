---
slug: maximum-swap
---
## Q
**LC 670 最大交换**｜Medium

非负整数 `num` 至多交换两位数字一次，求能得到的最大值。

## A
**一句话。** 贪心：从高位起，第一个右边有更大数字的位，换成那个最大数字的最右一次出现。

```python
def maximum_swap(num):
    digits = list(str(num))
    # 每个数字最后一次出现的下标
    last = {d: i for i, d in enumerate(digits)}
    for i, d in enumerate(digits):
        for big in "9876543210":      # 从最大的找起
            if big <= d:              # 右边没有更大的
                break
            if last.get(big, -1) > i:
                j = last[big]
                digits[i], digits[j] = digits[j], digits[i]
                return int("".join(digits))
    return num
```

**复杂度。** 时间 `O(10d)`，空间 `O(d)`。

**易错点。**
- 换最大数字的第一次出现：`1993` 得 `9193`，应为 `9913`。
- 候选从小到大找：`2736` 得 `3726`，应为 `7236`。
- 换完不返回：只能换一次，`2736` 继续换会得 `7632`。

**追问。**
- 至多交换 `k` 次？：没有简单贪心，按层 BFS 搜交换后的状态，`set` 去重。
- 有一遍扫描的写法吗？：从右向左维护最大数字的下标，遇到更小的数字就记一对，最后换最后记录的那一对。

**同模式。** LC 402 移掉 K 位数字、LC 738 单调递增的数字、LC 556 下一个更大元素 III、LC 321 拼接最大数
