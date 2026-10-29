---
id: tlc-3sum-closest-4-followup
node: a.3sum-closest
type: qa
step: 4
---
## Q
**LC 16 最接近的三数之和**｜追问

面试官接着问：（1）要返回具体的三个数，而不仅是和？（2）推广到 `k` 个数（4Sum Closest）？（3）有没有办法提前剪枝？

## A
1. **返回三个数。** 更新 `best` 的同时记录 `(nums[i], nums[lo], nums[hi])`。如果要原数组的下标，先 `order = sorted(range(n), key=nums.__getitem__)`，在排序后的值上做双指针，再用 `order` 映射回原下标。
2. **`k` 个数。** 外层套 `k - 2` 层循环，最内层仍是对撞双指针，总复杂度 `O(n^{k-1})`；也可以递归地写成 `k_sum_closest(nums, k, target)`，在 `k == 2` 时用双指针。
3. **剪枝。** 排序后，对固定的 `i`，最小的和是 `nums[i] + nums[i+1] + nums[i+2]`，最大的和是 `nums[i] + nums[-2] + nums[-1]`。最小和已经大于 `target`，后面的 `i` 只会更大，用它更新答案后可以结束；最大和仍小于 `target`，这个 `i` 下无需双指针。

**Python 提醒**：`nums.sort()` 原地排序并返回 `None`，会改动调用者的数组；`sorted(nums)` 返回新列表。函数入口处用 `nums = sorted(nums)` 是最安全的写法，也避免了在面试官的测试里出现"输入被改了"的意外。
