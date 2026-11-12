---
slug: tt-delete-window-balance-even-odd
---
## Q
**删除一个长度为 k 的窗口，使奇偶下标之和相等**｜Medium

删除 `nums` 中一段长度恰为 `k` 的连续子数组，剩余元素重新编号后要求偶数下标之和等于奇数下标之和。返回最小的窗口起点，没有则返回 `-1`（删空后两个和都是 `0`，算满足）。

## A
**一句话。** 按原下标奇偶加符号做前缀和，窗口左边贡献不变，右边整体左移 `k` 位，`k` 为奇数时符号翻转，差值为 `0` 即满足。

```python
def min_balanced_deletion(nums, k):
    n = len(nums)
    # pre[i]：前 i 个元素的「偶下标和 - 奇下标和」
    sign = (x if i % 2 == 0 else -x
            for i, x in enumerate(nums))
    pre = list(accumulate(sign, initial=0))
    flip = -1 if k % 2 else 1      # 右半左移 k 位，k 奇则奇偶互换
    for i in range(n - k + 1):
        left = pre[i]
        right = flip * (pre[n] - pre[i + k])
        if left + right == 0:
            return i
    return -1
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 右半不翻转：`[1,1,1,2,1]`、`k = 1` 删下标 `3` 剩 `[1,1,1,1]`，应得 `3`，不翻转得 `-1`。
- `range(n - k)`：漏掉窗口在末尾的情况。
- `pre` 少了 `initial=0`：所有下标错位一格，`pre[i + k]` 也取不到 `pre[n]`。

**追问。**
- 要所有满足的起点？：不要提前 `return`，收集成列表。
- 窗口长度不固定？：把 `pre` 按奇偶分类，找前缀和差为 `0` 的下标对，用哈希表。

**同模式。** LC 1664 生成平衡数组的方案数、LC 238 除自身以外数组的乘积、LC 724 寻找数组的中心下标、LC 560 和为 K 的子数组
