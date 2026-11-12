---
slug: codetop-supp-6
---
## Q
**补充题 6 手撕堆排序**｜Medium

手写堆排序，原地把整数数组升序排列，不用 `sorted`、`heapq`。

## A
**一句话。** 先原地建大根堆，再反复把堆顶换到未排序区末尾、堆缩小一格、对新堆顶下沉。

```python
def sort_array(nums):
    n = len(nums)

    def sift_down(p, size):        # 堆范围 nums[0:size]
        while (c := 2 * p + 1) < size:
            if c + 1 < size and \
                    nums[c+1] > nums[c]:
                c += 1            # 取较大的孩子
            if nums[p] >= nums[c]:
                break
            nums[p], nums[c] = nums[c], nums[p]
            p = c

    for i in range(n // 2 - 1, -1, -1):   # 建堆
        sift_down(i, n)
    for end in range(n - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]
        sift_down(0, end)
    return nums
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`。

**易错点。**
- 排序阶段下沉用 `size = n`：已排好的尾部被拉回堆里，`[5,2,3,1]` 得 `[3,5,1,2]`。
- 建堆从根往后下沉：子树还不是堆，应从最后一个非叶子节点向前到根。
- 不判 `child + 1 < size`：右孩子越界。

**追问。**
- 建堆为什么是 `O(n)`？：高度 `h` 的节点至多 `n / 2^(h+1)` 个，各下沉 `O(h)`，求和为 `O(n)`。
- 稳定吗？：不稳定，交换堆顶和末尾会打乱相等元素的次序。

**同模式。** LC 215 数组中的第 K 个最大元素、LC 347 前 K 个高频元素、LC 23 合并 K 个升序链表、LC 912 排序数组
