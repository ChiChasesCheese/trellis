---
id: tlc-merge-sorted-array-4-followup
node: p2.merge-sorted-array
type: qa
step: 4
---
## Q
**LC 88 合并两个有序数组**｜追问

面试官接着问：（1）相等元素时，`nums1` 和 `nums2` 的谁排前面，算不算稳定？（2）不想手写三指针，能不能用 Python 一两行完成？（3）如果是合并 `k` 个有序数组呢？

## A
1. **稳定性**：从后往前填，相等时取 `nums2` 的元素放在后面（`else` 分支），所以 `nums1` 的相等元素仍排在 `nums2` 的前面，等价于以 `nums1` 为主的稳定归并。如果判断写成 `nums1[i] >= nums2[j]`，相等时先放 `nums1` 的，顺序就反了。
2. **库函数写法**：`nums1[m:] = nums2` 把尾部占位换成 `nums2`，再 `nums1.sort()`。Python 的 Timsort 会识别出两段已有序的连续片段并直接归并，比较次数接近 `O(m + n)`。它简洁、可读，但依赖实现细节；面试里先写三指针，再提这一种。

```python
def merge_with_sort(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    nums1[m:] = nums2
    nums1.sort()
```

3. **`k` 个有序数组**：三指针不再够用，改用最小堆（`heapq.merge(*arrays)` 或手写堆），`O(N log k)`；或两两合并（分治）。

**Python 提醒**：`nums1[m:] = nums2` 是切片赋值，修改的是原列表对象，调用者能看到结果；`nums1 = nums1[:m] + nums2` 只是让局部名字指向新列表，调用者的 `nums1` 不变。题目要求原地修改，必须用切片赋值或下标赋值。
