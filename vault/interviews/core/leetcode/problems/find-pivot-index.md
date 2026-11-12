---
slug: find-pivot-index
---
## Q
**LC 724 寻找数组的中心下标**｜Easy

找最靠左的下标，使其左侧元素和等于右侧元素和（空侧视为 `0`），不存在返回 `-1`。

## A
**一句话。** 前缀和：已知总和 `total`，扫到 `i` 时右侧和为 `total - left - nums[i]`，相等即是答案。

```python
def pivot_index(nums):
    total, left = sum(nums), 0
    for i, x in enumerate(nums):
        if left == total - left - x:
            return i
        left += x            # 先判断再累加
    return -1
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 先累加再判断，或没排除 `nums[i]`：`[1,7,3,6,5,6]` 得 `-1`，应为 `3`。
- 用「左和超过总和一半就停」剪枝：含负数时前缀和不单调，会漏答案。
- 初始 `left` 写成 `nums[0]`：中心在最左端时左侧是空，应为 `0`。

**追问。**
- 要返回所有中心下标？：不提前返回，收集全部命中。

**同模式。** LC 1732 找到最高海拔、LC 560 和为 K 的子数组、LC 238 除了自身以外数组的乘积、LC 303 区域和检索
