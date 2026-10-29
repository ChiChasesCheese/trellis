---
id: tlc-first-missing-positive-5-alt
node: a.first-missing-positive
type: qa
step: 5
---
## Q
**LC 41 缺失的第一个正数**｜另一种解法

除了把数交换回「家」，还有没有同样 `O(n)` 时间、`O(1)` 空间的做法？它和交换法比各有什么取舍？

## A
**符号标记法。** 用元素的正负当作「这个值出现过」的标记位：先把非正数换成越界的哨兵 `n + 1`；再扫描，对每个 `1 <= |x| <= n`，把 `nums[|x| - 1]` 变成负数；最后第一个仍为正的位置 `i`，说明 `i + 1` 没出现过。

```python
def first_missing_positive(nums: list[int]) -> int:
    n = len(nums)
    for i, x in enumerate(nums):
        if x <= 0:
            nums[i] = n + 1             # 非正数不会影响答案，先换成越界的哨兵
    for x in nums:
        v = abs(x)
        if v <= n:
            nums[v - 1] = -abs(nums[v - 1])     # 用符号当"v 出现过"的标记
    for i, x in enumerate(nums):
        if x > 0:                       # 没被标成负数：i + 1 没出现
            return i + 1
    return n + 1
```

`[3,4,-1,1]` → `2`，`[7,8,9,11,12]` → `1`，`[1,2,0]` → `3`。

**怎么选。**
- 交换法：代码更短，不需要 `abs`；数组被打乱成「接近排序」的样子，之后还能直接用。
- 符号标记法：不移动元素，遍历顺序固定，不会因为交换写法出错（没有死循环风险）；注意读值时必须取 `abs`，因为同一个位置可能已被标成负数。
- 两者都修改输入。不允许修改时，改用集合 `O(n)` 空间。
