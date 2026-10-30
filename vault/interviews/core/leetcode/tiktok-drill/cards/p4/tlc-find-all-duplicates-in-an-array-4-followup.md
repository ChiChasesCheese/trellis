---
id: tlc-find-all-duplicates-in-an-array-4-followup
node: p4.find-all-duplicates-in-an-array
type: qa
step: 4
---
## Q
**LC 442 数组中重复的数据**｜追问

面试官接着问：（1）做完以后能不能把输入还原？（2）输入是只读的，怎么办？（3）如果每个数可能出现很多次，要统计每个重复数出现几次？

## A
1. **还原输入**：标记法把一部分元素改成了负数。结果收集完后，再扫一遍把符号还原。
```python
def find_duplicates_restore(nums: list[int]) -> list[int]:
    res: list[int] = []
    for x in nums:
        i = abs(x) - 1
        if nums[i] < 0:
            res.append(abs(x))
        else:
            nums[i] = -nums[i]
    for i in range(len(nums)):
        nums[i] = abs(nums[i])                 # 还原符号
    return res
```
`[4,3,2,7,8,2,3,1]` 返回 `[2,3]`，之后 `nums` 变回原样。
2. **输入只读**：不能原地标记，退回 `O(n)` 额外空间：`seen` 集合，或布尔数组；也可以排序副本后比较相邻项，`O(n log n)`。想保持 `O(1)` 空间又不改输入，没有简单办法。
3. **出现多次且要计数**：一位符号信息不够了。用 `Counter`（`O(n)` 空间），或者原地排序后统计相邻相同段的长度（`O(n log n)` 时间、`O(1)` 额外空间）。

**Python 提醒**：`for x in nums` 遍历时 `x` 是读取瞬间的元素值，不是下标；中途改 `nums[i]` 会影响后面读到的 `x`，所以才需要 `abs`。用 `enumerate` 或下标循环时同样如此。
