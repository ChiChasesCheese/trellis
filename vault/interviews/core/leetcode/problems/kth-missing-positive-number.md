---
slug: kth-missing-positive-number
---
## Q
**LC 1539 第 k 个缺失的正整数**｜Easy

严格升序的正整数数组 `arr`，求缺失的第 `k` 个正整数。

## A
**一句话。** `arr[i]` 之前缺 `arr[i]-(i+1)` 个数且单调不减，二分第一个缺失数 `>= k` 的下标 `lo`，答案是 `lo + k`。

```python
def find_kth_positive(arr, k):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] - (mid + 1) >= k:   # arr[mid] 前已缺够 k 个
            hi = mid
        else:
            lo = mid + 1
    return lo + k    # 答案前有 lo 个数在 arr 里
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 缺失个数漏掉 `+1`，写成 `arr[mid]-mid`：`([1],1)` 得 `1`，应为 `2`。
- 比较写成 `> k`：缺失数恰好为 `k` 时答案在该元素前，`([2],1)` 得 `2`，应为 `1`。
- 二分里直接返回 `arr[lo]-…`：`lo == n` 时越界，用 `lo + k`。

**追问。**
- 线性写法？：`for x in arr: if x <= k: k += 1`，最后返回 `k`，`O(n)`。
- `k` 极大呢？：二分仍是 `O(log n)`，答案最大 `k + n`。

**同模式。** LC 268 丢失的数字、LC 41 缺失的第一个正数、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 704 二分查找
