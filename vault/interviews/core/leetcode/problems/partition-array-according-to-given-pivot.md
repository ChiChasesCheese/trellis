---
slug: partition-array-according-to-given-pivot
---
## Q
**LC 2161 根据给定数字划分数组**｜Medium

整数数组 `nums` 和 `pivot`。重排使得所有小于 `pivot` 的在前，等于的居中，大于的在后；小于组、大于组内部保持原来的相对顺序。返回重排后的数组。

## A
**一句话。** 稳定三路划分：按原顺序分别收集小于、等于、大于的元素再拼起来。

```python
def pivot_array(nums, pivot):
    return ([x for x in nums if x < pivot]
            + [x for x in nums if x == pivot]
            + [x for x in nums if x > pivot])
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用荷兰国旗原地交换：交换会打乱同组内的原顺序，题目要求稳定。
- 等于组漏掉：三组之和必须是 `n`。

**追问。**
- 不稳定也行时能原地吗？：三指针荷兰国旗，`O(1)` 空间，见 LC 75。

**同模式。** LC 75 颜色分类、LC 922 按奇偶排序数组 II、LC 283 移动零
