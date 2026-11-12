---
slug: subarray-with-elements-greater-than-varying-threshold
---
## Q
**LC 2334 元素值大于变化阈值的子数组**｜Hard

找长度为 `k` 的子数组，使每个元素都大于 `threshold / k`，返回任意一个合法的长度，没有返回 `-1`。

## A
**一句话。** 条件等价于「最小值 `h` 满足 `h*k > threshold`」，用单调栈求每个元素当最小值时的最大宽度 `k`。

```python
def valid_subarray_size(nums, threshold):
    st = []                        # 下标栈，值严格递增
    for i, x in enumerate(chain(nums, (0,))):   # 哨兵 0
        while st and nums[st[-1]] >= x:
            h = nums[st.pop()]
            left = st[-1] if st else -1
            k = i - left - 1       # h 当最小值的最大宽度
            if h * k > threshold:  # 乘过去避免浮点
                return k
        st.append(i)
    return -1
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 写成 `h * k >= threshold`：`nums = [2]`、`threshold = 2` 会返回 `1`，应为 `-1`。
- 宽度写成 `i - left`：`i` 是右边第一个更小的位置，不在窗口里，要再减 `1`。

**追问。**
- 要最大的合法长度怎么改？：不提前返回，对满足条件的 `k` 取最大。
- 还有别的做法吗？：按值从大到小点亮元素并并查集合并，连通块大小就是最大宽度。

**同模式。** LC 84 柱状图中最大的矩形、LC 85 最大矩形、LC 907 子数组的最小值之和、LC 739 每日温度
