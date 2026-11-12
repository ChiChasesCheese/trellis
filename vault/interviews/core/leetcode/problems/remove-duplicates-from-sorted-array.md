---
slug: remove-duplicates-from-sorted-array
---
## Q
**LC 26 删除有序数组中的重复项**｜Easy

有序数组 `nums`，原地去重使每个元素只出现一次，返回唯一元素个数 `k`，前 `k` 个位置放去重结果。

## A
**一句话。** 快慢指针，慢指针 `k` 是下一个写入位，当前元素和已保留的最后一个不同就写入。

```python
def remove_duplicates(nums):
    k = 1       # nums[:k] 已去重，nums[0] 必留
    for i in range(1, len(nums)):
        if nums[i] != nums[k - 1]:
            nums[k] = nums[i]
            k += 1
    return k
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只返回 `len(set(nums))`：数对了，但 `nums` 没改，`[0,0,1,1]` 前两项仍是 `[0,0]`。
- `k` 从 `0` 起并比较 `nums[k-1]`：`-1` 是末元素，`[1,1,1]` 返回 `0`，应为 `1`。
- 边遍历边 `del nums[i]`：下标错位漏掉相邻重复，还是 `O(n²)`。

**追问。**
- 每个值最多保留两次（LC 80）怎么改？：改比较 `nums[k-2]`，`k` 从 `2` 起。

**同模式。** LC 80 删除有序数组中的重复项 II、LC 27 移除元素、LC 283 移动零、LC 82 删除排序链表中的重复元素 II
