---
id: tlc-next-permutation-4-followup
node: a.next-permutation
type: qa
step: 4
---
## Q
**LC 31 下一个排列**｜追问

面试官接着问：（1）怎么求**上一个**排列？（2）要求第 `k` 个排列，难道调用 `k` 次吗？（3）数组元素有重复，结果还对吗？

## A
1. **上一个排列**：把所有大小关系反过来。从右往左找第一个 `nums[i] > nums[i+1]` 的位置 `i`；在右边的升序段里找比 `nums[i]` 小的最大值，交换；把右段翻转成降序。找不到 `i` 时整个数组翻转（升序变降序）。
2. **第 `k` 个排列（LC 60）**：不要重复 `k` 次。第一位由 `(k-1) // (n-1)!` 决定，余数再决定下一位，`O(n^2)`。如果已经给出某个排列、要往后跳 `k` 个，才用「康托展开」转成序号加 `k` 再转回去。
3. **有重复值**：本解法天然支持。重复值只影响比较符号：找升位时，相等也继续左移（`nums[i] >= nums[i+1]`）；找交换对象时，`nums[j] <= nums[i]` 就继续左移，直到遇到严格更大的数。`[1,1,5]` → `[1,5,1]`；`[1,2,2]` → `[2,1,2]`。

```python
def prev_permutation(nums: list[int]) -> None:
    i = len(nums) - 2
    while i >= 0 and nums[i] <= nums[i + 1]:
        i -= 1
    if i >= 0:
        j = len(nums) - 1
        while nums[j] >= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    nums[i + 1:] = nums[i + 1:][::-1]
```

**Python 提醒**：对 `list` 做切片赋值 `nums[a:] = ...` 可以改变长度，`i = -1` 时 `nums[0:]` 才是整个数组；写成反向切片 `nums[:i:-1]` 时，`i = -1` 会得到空列表而不是整个数组，这是最常见的下标陷阱。
