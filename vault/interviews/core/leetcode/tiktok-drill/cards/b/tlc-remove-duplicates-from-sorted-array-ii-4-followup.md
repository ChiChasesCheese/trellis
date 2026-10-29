---
id: tlc-remove-duplicates-from-sorted-array-ii-4-followup
node: b.remove-duplicates-from-sorted-array-ii
type: qa
step: 4
---
## Q
**LC 80 删除有序数组中的重复项 II**｜追问

面试官接着问：（1）改成每个值最多保留 `k` 个？（2）数组**不保证有序**，但要保持原顺序、每个值最多两个？（3）调用者不看返回的长度，要求 `nums` 本身被截断？

## A
1. **至多 `k` 个**：把两处 `2` 换成 `k`，`k = 1` 就是 LC 26：

```python
def remove_duplicates_k(nums: list[int], k: int) -> int:
    w = 0
    for x in nums:
        if w < k or x != nums[w - k]:      # 结果里倒数第 k 个与 x 相同，说明已有 k 个 x
            nums[w] = x
            w += 1
    return w
```
   运行：`[1,1,1,2,2,3]`、`k = 1` → `3`（前三个 `[1,2,3]`）；`[0,0,1,1,1,1,2,3,3]`、`k = 3` → `8`（前八个 `[0,0,1,1,1,2,3,3]`）。
2. **无序**：相同值不再相邻，不能只看结果末尾。用 `Counter` 记每个值已保留的次数，`seen[x] < 2` 才写入：时间 `O(n)`，额外空间 `O(不同值个数)`。想保持 `O(1)` 空间只能先排序，但会改变原顺序。
3. **真正截断**：返回长度之后加一行 `del nums[w:]`（`O(n - w)`），或者 `nums[:] = nums[:w]`。注意不能写 `nums = nums[:w]`，那只是让局部变量指向新列表，调用者看不到。

**Python 提醒**：原地修改列表要用切片赋值 `nums[:] = ...` 或下标赋值；`nums = ...` 只是重新绑定名字，不改变调用者持有的那个列表对象。
