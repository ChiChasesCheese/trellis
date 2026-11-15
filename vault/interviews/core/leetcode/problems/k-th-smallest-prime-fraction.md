---
slug: k-th-smallest-prime-fraction
---
## Q
**LC 786 第 K 个最小的质数分数**｜Medium

递增数组 `arr` 由 1 和若干质数组成，所有 `i < j` 构成分数 `arr[i]/arr[j]`，求第 `k` 小的分数，返回 `[分子, 分母]`。

## A
**一句话。** 固定分母 `arr[j]`，分子从小到大就是一条递增链；`n-1` 条链做多路归并，最小堆弹出 `k-1` 次，堆顶就是第 `k` 小。

```python
def kth_smallest_prime_fraction(arr, k):
    n = len(arr)
    # 每个分母 j 一条递增链：arr[0]/arr[j] < arr[1]/arr[j] < …
    h = [(arr[0] / arr[j], 0, j) for j in range(1, n)]
    heapify(h)
    for _ in range(k - 1):
        _, i, j = heappop(h)
        if i + 1 < j:          # 链上下一个分数
            heappush(h, (arr[i + 1] / arr[j], i + 1, j))
    _, i, j = h[0]
    return [arr[i], arr[j]]
```

**复杂度。** 时间 `O((n + k) log n)`，空间 `O(n)`。

**易错点。**
- 把所有 `n²/2` 个分数都放进堆：`n = 1000` 时 50 万个，慢且占内存。
- 链的终点写成 `i + 1 < n`：分子下标必须小于分母下标 `j`。

**追问。**
- `k` 很大时更快？：二分分数值 `x`，双指针数出 `<= x` 的分数个数并记下最大的那个，`O(n log W)`。
- 浮点比较安全吗？：分数互不相等且分母不超过 `3·10^4`，双精度足够；要严格可比 `a·d < b·c`。

**同模式。** LC 373 查找和最小的 K 对数字、LC 378 有序矩阵中第 K 小的元素、LC 23 合并 K 个升序链表
