---
slug: find-in-mountain-array
---
## Q
**LC 1095 山脉数组中查找目标值**｜Hard

山脉数组先严格升后严格降，只能通过 `get(i)` 读元素、`length()` 读长度，且 `get` 至多调用 100 次。返回目标值的最小下标，没有则 `-1`。

## A
**一句话。** 三次二分：先二分找峰顶，再在升序段里找，找不到再到降序段里找（降序段把比较方向取反）。

```python
def find_in_mountain_array(target, arr):
    n = arr.length()
    lo, hi = 0, n - 1
    while lo < hi:                      # 找峰顶
        mid = (lo + hi) // 2
        if arr.get(mid) < arr.get(mid + 1):
            lo = mid + 1                # 还在上坡
        else:
            hi = mid
    peak = lo
    def search(lo, hi, sign):           # sign=1 升段，-1 降段
        while lo <= hi:
            mid = (lo + hi) // 2
            v = arr.get(mid)
            if v == target:
                return mid
            if sign * v < sign * target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
    i = search(0, peak, 1)              # 先升段，下标更小
    return i if i != -1 else search(peak + 1, n - 1, -1)
```

**复杂度。** 时间 `O(log n)`，`get` 调用约 `3·log n` 次，空间 `O(1)`。

**易错点。**
- 先搜降序段：目标可能在两段都出现，要返回最小下标，所以先搜升序段。
- 峰顶二分用 `lo <= hi`：会越界，`mid + 1` 要保证存在，用 `lo < hi`。
- 降序段仍按升序比较：方向相反，用 `sign` 取反，或手写第二个版本。

**追问。**
- 为什么能二分找峰顶？：比较 `a[mid]` 与 `a[mid+1]` 就知道在上坡还是下坡，每次丢弃一半。
- `get` 调用有限制，怎么再省？：缓存已读的值（字典），同一下标不重复调用。

**同模式。** LC 852 山脉数组的峰顶索引、LC 162 寻找峰值、LC 33 搜索旋转排序数组、LC 1671 得到山形数组的最少删除次数
