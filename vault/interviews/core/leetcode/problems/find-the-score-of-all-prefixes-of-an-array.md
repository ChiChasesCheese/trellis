---
slug: find-the-score-of-all-prefixes-of-an-array
---
## Q
**LC 2640 一个数组所有前缀的分数**｜Medium

`conver[i] = nums[i] + max(nums[0..i])`，一个数组的分数是 `conver` 之和。返回 `ans`，其中 `ans[i]` 是前缀 `nums[0..i]` 的分数。

## A
**一句话。** 两层前缀：先前缀最大值得到 `conver`，再对 `conver` 做前缀和。

```python
def find_prefix_score(nums):
    pmax = accumulate(nums, max)           # 前缀最大值
    conver = (x + m for x, m in zip(nums, pmax))
    return list(accumulate(conver))
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`（不计输出）。

**易错点。**
- 前缀最大值写成全局最大值：`[2,3,7,5,10]` 的 `ans[0]` 得 `12`，应为 `4`。
- 写成 `前缀和 + 前缀最大值`：每个位置都要加各自的前缀最大值，`ans[2]` 得 `19`，应为 `24`。

**追问。**
- 数据流式到来？：只留 `run_max` 和 `total` 两个变量，每个元素 `O(1)`。
- Java / C++ 有什么坑？：和会超 32 位，要用 `long`。

**同模式。** LC 1480 一维数组的动态和、LC 724 寻找数组的中心下标、LC 238 除自身以外数组的乘积、LC 121 买卖股票的最佳时机
