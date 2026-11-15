---
slug: longest-turbulent-subarray
---
## Q
**LC 978 最长湍流子数组**｜Medium

若相邻元素的比较符号逐项交替（`<`、`>` 轮流），子数组称为湍流。给数组 `arr`，返回最长湍流子数组的长度。

## A
**一句话。** 记以当前元素结尾、最后一步是「升」或「降」的最长湍流长度：升接在降后，降接在升后，相等则都重置为 1。

```python
def max_turbulence_size(arr):
    ans = up = down = 1               # 以 i 结尾，最后一步 升 / 降
    for i in range(1, len(arr)):
        if arr[i] > arr[i - 1]:
            up, down = down + 1, 1
        elif arr[i] < arr[i - 1]:
            up, down = 1, up + 1
        else:
            up = down = 1             # 相等：断开
        ans = max(ans, up, down)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 更新 `up` 后再用新的 `up` 更新 `down`：要用旧值，所以同时赋值 `up, down = down + 1, 1`。
- 把相等当成一个转折：相等时湍流断开，两个计数都回到 `1`。
- 与摆动序列混淆：这里要求子数组（连续），那题是子序列。

**追问。**
- 怎么用滑动窗口做？：维护左端，遇相等左端设成 `i`，遇两连升或两连降左端设成 `i-1`。
- 想要返回具体区间？：记下 `ans` 更新时的右端，往回数 `ans` 个。

**同模式。** LC 376 摆动序列、LC 674 最长连续递增序列、LC 413 等差数列划分、LC 845 数组中的最长山脉
