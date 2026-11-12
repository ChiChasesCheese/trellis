---
slug: find-k-pairs-with-smallest-sums
---
## Q
**LC 373 查找和最小的 K 对数字**｜Medium

两个升序数组 `nums1`、`nums2`，各取一个数组成数对，返回和最小的 `k` 对。

## A
**一句话。** 每个 `nums1[i]` 与 `nums2` 配成一条升序序列，小根堆放各序列的当前头，弹出一个再补同序列的下一个。

```python
def k_smallest_pairs(nums1, nums2, k):
    # 堆元素 (和, i, j)；最多放 k 行
    heap = [(nums1[i] + nums2[0], i, 0)
            for i in range(min(k, len(nums1)))]
    heapify(heap)
    res = []
    while heap and len(res) < k:
        _, i, j = heappop(heap)
        res.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):   # 只补同行下一个，不会重复
            s = nums1[i] + nums2[j + 1]
            heappush(heap, (s, i, j + 1))
    return res
```

**复杂度。** 时间 `O(k log min(k,n))`，空间 `O(min(k,n))`。

**易错点。**
- 全部 `n·m` 对一次入堆：`10^5×10^5` 内存和时间都爆。
- 弹出后既补 `(i+1,j)` 又补 `(i,j+1)` 且不去重：`(i+1,j+1)` 入堆两次，结果出现重复数对。
- 补下一个前不查 `j+1 < len(nums2)`：`nums2=[3]` 时 `IndexError`。

**追问。**
- 为什么初始只放前 `min(k,n)` 行？：第 `k+1` 行以后的头不会早于前 `k` 行的头被弹出，那时已够 `k` 个。
- 去重的另一种写法？：弹出 `(i,j)` 时补 `(i,j+1)`，且仅当 `j==0` 才补 `(i+1,0)`，起始堆只有一个元素。

**同模式。** LC 378 有序矩阵中第 K 小的元素、LC 23 合并 K 个升序链表、LC 719 找出第 K 小的数对距离、LC 786 第 K 个最小的质数分数
