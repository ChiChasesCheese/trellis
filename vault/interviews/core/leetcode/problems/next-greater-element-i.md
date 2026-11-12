---
slug: next-greater-element-i
---
## Q
**LC 496 下一个更大元素 I**｜Easy

`nums1` 是 `nums2` 的子集（元素互不相同），对 `nums1` 每个数求它在 `nums2` 中右侧第一个更大的数，没有则为 `-1`。

## A
**一句话。** 对 `nums2` 做一趟递减单调栈，被弹出时遇到的当前数就是答案，存进字典再查表。

```python
def next_greater_element(nums1, nums2):
    nxt = {}                     # nums2 中每个数 -> 下一个更大元素
    stack = []                   # 还没答案的数，自底向上递减
    for x in nums2:
        while stack and stack[-1] < x:
            nxt[stack.pop()] = x
        stack.append(x)
    return [nxt.get(x, -1) for x in nums1]
```

**复杂度。** 时间 `O(m+n)`，空间 `O(n)`。

**易错点。**
- `while` 写成 `if`：只弹一个，`([3,2],[3,2,1,4])` 得 `[-1,-1]`，应为 `[4,4]`。
- 取不到时 `KeyError`：栈里剩下的数没有答案，要 `nxt.get(x, -1)`。

**追问。**
- 循环数组（LC 503）？：下标取模遍历两遍，第二遍只弹栈不入栈。
- 有重复元素呢？：字典不能按值存，改存下标并按下标填答案。

**同模式。** LC 503 下一个更大元素 II、LC 739 每日温度、LC 901 股票价格跨度、LC 84 柱状图中最大的矩形
