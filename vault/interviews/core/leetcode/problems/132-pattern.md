---
slug: 132-pattern
---
## Q
**LC 456 132 模式**｜Medium

判断数组里是否存在下标 `i < j < k` 使 `nums[i] < nums[k] < nums[j]`。`n` 到 `2·10^5`。

## A
**一句话。** 从右往左扫，单调递减栈存候选的 `nums[j]`，被弹出的最大值就是最好的 `nums[k]`（`third`），遇到比 `third` 小的数即成立。

```python
def find132pattern(nums):
    st = []                # 单调递减，候选的 nums[j]
    third = -inf           # 已有更大的 j 罩着的最大 nums[k]
    for x in reversed(nums):
        if x < third:      # x 当 nums[i]
            return True
        while st and st[-1] < x:
            third = st.pop()   # x 当 nums[j]，弹出的当 nums[k]
        st.append(x)
    return False
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 从左往右扫找「前面最小值」再配栈：能做但要额外维护前缀最小，容易把 `i` 和 `k` 的大小关系弄反。
- 弹栈条件写成 `<=`：相等的数被弹出当 `third`，`[1,1,1]` 后接更小的数会误判；`nums[k] < nums[j]` 要严格。

**追问。**
- 为什么 `third` 只增不减？：每次被弹出的都小于当前 `x`，而 `x` 留在栈里继续罩着它；之后 `third` 只会被更大的弹出值刷新。
- 正向写法？：前缀最小值 `pre[j]` 当 `nums[i]`，从右往左单调栈找 `(pre[j], nums[j])` 之间的 `nums[k]`。

**同模式。** LC 739 每日温度、LC 496 下一个更大元素 I、LC 84 柱状图中最大的矩形
